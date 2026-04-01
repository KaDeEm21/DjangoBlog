from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import Http404, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm, LoginForm, PostForm, ProfileForm, RegistrationForm
from .models import Category, Comment, Like, Post, Profile, Tag

User = get_user_model()


def get_client_ip(request):
    forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded_for:
        return forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '')


def get_base_post_queryset():
    return (
        Post.objects.filter(is_published=True)
        .select_related('category', 'author')
        .prefetch_related('tags')
        .annotate(
            like_count=Count('likes', distinct=True),
            approved_comment_count=Count('comments', filter=Q(comments__is_approved=True), distinct=True),
        )
    )


def get_sidebar_context():
    categories = (
        Category.objects.annotate(posts_count=Count('posts', filter=Q(posts__is_published=True), distinct=True))
        .filter(posts_count__gt=0)
        .order_by('name')
    )
    tags = Tag.objects.order_by('name')
    return {
        'categories': categories,
        'tags': tags,
    }


def get_user_posts_queryset(user):
    return (
        user.posts.select_related('category')
        .prefetch_related('tags')
        .annotate(
            like_count=Count('likes', distinct=True),
            approved_comment_count=Count('comments', filter=Q(comments__is_approved=True), distinct=True),
        )
        .order_by('-created_at')
    )


def get_user_comments_queryset(user):
    return (
        Comment.objects.filter(post__author=user)
        .select_related('post')
        .order_by('-created_at')
    )


def build_post_detail_context(post, request, comment_form=None):
    related_posts = (
        get_base_post_queryset()
        .filter(category=post.category)
        .exclude(pk=post.pk)[:3]
    )
    comments = post.comments.filter(is_approved=True).order_by('created_at')
    return {
        'post': post,
        'related_posts': related_posts,
        'comments': comments,
        'has_liked': Like.objects.filter(post=post, ip_address=get_client_ip(request)).exists(),
        'comment_form': comment_form or CommentForm(post=post),
    }


def post_list(request):
    category_slug = request.GET.get('category')
    tag_slug = request.GET.get('tag')
    sort_by = request.GET.get('sort', 'newest')

    posts = get_base_post_queryset()
    if category_slug:
        posts = posts.filter(category__slug=category_slug)
    if tag_slug:
        posts = posts.filter(tags__slug=tag_slug)

    if sort_by == 'popular':
        posts = posts.order_by('-like_count', '-created_at')
    elif sort_by == 'commented':
        posts = posts.order_by('-approved_comment_count', '-created_at')
    else:
        posts = posts.order_by('-created_at')

    paginator = Paginator(posts, 10)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'page_obj': page_obj,
        'post_count': paginator.count,
        'featured_posts': posts.filter(is_featured=True)[:3],
        'selected_category': category_slug,
        'selected_tag': tag_slug,
        'selected_sort': sort_by,
    }
    context.update(get_sidebar_context())
    return render(request, 'blog/post_list.html', context)


def post_detail(request, slug):
    post = get_base_post_queryset().filter(slug=slug).first()
    if not post:
        raise Http404('Post not found')
    return render(request, 'blog/post_detail.html', build_post_detail_context(post, request))


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = get_base_post_queryset().filter(category=category).order_by('-created_at')
    paginator = Paginator(posts, 9)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'blog/category_detail.html', {'category': category, 'page_obj': page_obj})


def tag_detail(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = get_base_post_queryset().filter(tags=tag).order_by('-created_at')
    paginator = Paginator(posts, 9)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'blog/tag_detail.html', {'tag': tag, 'page_obj': page_obj})


def search(request):
    query = request.GET.get('q', '').strip()
    posts = get_base_post_queryset()
    if query:
        posts = posts.filter(
            Q(title__icontains=query)
            | Q(content__icontains=query)
            | Q(category__name__icontains=query)
            | Q(tags__name__icontains=query)
            | Q(author__username__icontains=query)
        ).distinct()
    paginator = Paginator(posts.order_by('-created_at'), 9)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'blog/search.html', {'page_obj': page_obj, 'query': query})


def contact(request):
    return render(request, 'blog/contact.html')


def like_post(request, slug):
    if request.method == 'POST':
        post = get_object_or_404(Post, slug=slug, is_published=True)
        user_ip = get_client_ip(request)
        existing_like = Like.objects.filter(post=post, ip_address=user_ip).first()
        if existing_like:
            existing_like.delete()
        else:
            Like.objects.create(post=post, ip_address=user_ip)
    return redirect('post_detail', slug=slug)


@login_required(login_url='login')
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.is_published = True
            post.is_featured = False
            post.save()
            form.save_m2m()
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm()

    return render(request, 'blog/create_post.html', {'form': form})


@login_required(login_url='login')
def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)

    return render(
        request,
        'blog/create_post.html',
        {
            'form': form,
            'form_title': 'Edytuj post',
            'submit_label': 'Zapisz zmiany',
            'cancel_url': 'my_posts',
        },
    )


@login_required(login_url='login')
def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug, author=request.user)
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    post.delete()
    return redirect('my_posts')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('post_list')
            form.add_error(None, 'Niepoprawne dane logowania')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('post_list')


@login_required(login_url='login')
def profile(request):
    profile_obj, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile_obj)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile_obj)

    authored_posts = get_user_posts_queryset(request.user)
    recent_comments = get_user_comments_queryset(request.user)[:5]
    top_post = authored_posts.order_by('-like_count', '-approved_comment_count', '-created_at').first()
    return render(
        request,
        'registration/profile.html',
        {
            'form': form,
            'authored_posts': authored_posts[:5],
            'authored_posts_count': authored_posts.count(),
            'featured_posts_count': authored_posts.filter(is_featured=True).count(),
            'likes_received_count': Like.objects.filter(post__author=request.user).count(),
            'comments_received_count': Comment.objects.filter(post__author=request.user, is_approved=True).count(),
            'recent_comments': recent_comments,
            'top_post': top_post,
        },
    )


@login_required(login_url='login')
def my_posts(request):
    query = request.GET.get('q', '').strip()
    category_slug = request.GET.get('category', '').strip()
    featured = request.GET.get('featured', '').strip()

    posts = get_user_posts_queryset(request.user)
    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(content__icontains=query))
    if category_slug:
        posts = posts.filter(category__slug=category_slug)
    if featured == '1':
        posts = posts.filter(is_featured=True)

    paginator = Paginator(posts, 10)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(
        request,
        'blog/my_posts.html',
        {
            'page_obj': page_obj,
            'query': query,
            'selected_category': category_slug,
            'selected_featured': featured,
            'categories': Category.objects.filter(posts__author=request.user).distinct().order_by('name'),
        },
    )


@login_required(login_url='login')
def my_comments(request):
    comments = get_user_comments_queryset(request.user)
    status = request.GET.get('status', '').strip()
    query = request.GET.get('q', '').strip()

    if status == 'approved':
        comments = comments.filter(is_approved=True)
    elif status == 'hidden':
        comments = comments.filter(is_approved=False)

    if query:
        comments = comments.filter(
            Q(content__icontains=query)
            | Q(name__icontains=query)
            | Q(post__title__icontains=query)
        )

    paginator = Paginator(comments, 12)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(
        request,
        'blog/my_comments.html',
        {
            'page_obj': page_obj,
            'selected_status': status,
            'query': query,
            'approved_count': get_user_comments_queryset(request.user).filter(is_approved=True).count(),
            'hidden_count': get_user_comments_queryset(request.user).filter(is_approved=False).count(),
        },
    )


@login_required(login_url='login')
def toggle_comment_approval(request, pk):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    comment = get_object_or_404(Comment, pk=pk, post__author=request.user)
    comment.is_approved = not comment.is_approved
    comment.save(update_fields=['is_approved'])
    return redirect(request.POST.get('next') or 'my_comments')


@login_required(login_url='login')
def delete_comment(request, pk):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    comment = get_object_or_404(Comment, pk=pk, post__author=request.user)
    comment.delete()
    return redirect(request.POST.get('next') or 'my_comments')


def author_detail(request, username):
    author = get_object_or_404(User, username=username)
    profile_obj, _ = Profile.objects.get_or_create(user=author)
    posts = get_base_post_queryset().filter(author=author).order_by('-created_at')
    paginator = Paginator(posts, 9)
    page_obj = paginator.get_page(request.GET.get('page'))
    top_post = posts.order_by('-like_count', '-approved_comment_count', '-created_at').first()
    recent_posts = posts[:3]
    return render(
        request,
        'blog/author_detail.html',
        {
            'author_obj': author,
            'profile_obj': profile_obj,
            'page_obj': page_obj,
            'likes_received_count': Like.objects.filter(post__author=author).count(),
            'comments_received_count': Comment.objects.filter(post__author=author, is_approved=True).count(),
            'featured_posts_count': posts.filter(is_featured=True).count(),
            'top_post': top_post,
            'recent_posts': recent_posts,
        },
    )


def comment_create(request, slug):
    post = get_object_or_404(get_base_post_queryset(), slug=slug)
    if request.method != 'POST':
        return redirect('post_detail', slug=slug)

    form = CommentForm(request.POST, post=post)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.is_approved = False
        comment.save()
        messages.success(request, 'Komentarz został zapisany i czeka na akceptację autora.')
        return redirect('post_detail', slug=slug)

    return render(request, 'blog/post_detail.html', build_post_detail_context(post, request, form))
