from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Category, Comment, Like, Post, Profile, Tag

User = get_user_model()


class BlogModelTests(TestCase):
    def test_profile_created_for_new_user(self):
        user = User.objects.create_user(username='anna', email='anna@example.com', password='Secret123')
        self.assertTrue(Profile.objects.filter(user=user).exists())

    def test_post_slug_is_generated_and_unique(self):
        first = Post.objects.create(title='Testowy wpis', content='a' * 80, is_published=True)
        second = Post.objects.create(title='Testowy wpis', content='b' * 80, is_published=True)

        self.assertEqual(first.slug, 'testowy-wpis')
        self.assertEqual(second.slug, 'testowy-wpis-2')


class BlogViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='autor',
            email='autor@example.com',
            password='Secret123',
        )
        self.category = Category.objects.create(name='Python', slug='python')
        self.tag = Tag.objects.create(name='django', slug='django')
        self.post = Post.objects.create(
            title='Pierwszy wpis',
            content='To jest bardzo dluga tresc posta na potrzeby testu. ' * 3,
            category=self.category,
            author=self.user,
            is_published=True,
        )
        self.post.tags.add(self.tag)

    def test_create_post_requires_login(self):
        response = self.client.get(reverse('create_post'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_logged_user_can_create_post(self):
        self.client.login(username='autor', password='Secret123')
        response = self.client.post(
            reverse('create_post'),
            {
                'title': 'Nowy wpis',
                'image_url': 'https://example.com/image.jpg',
                'content': 'To jest tresc nowego wpisu o odpowiedniej dlugosci. ' * 2,
                'category': self.category.pk,
                'tags': [self.tag.pk],
            },
        )

        created_post = Post.objects.get(title='Nowy wpis')
        self.assertRedirects(response, reverse('post_detail', args=[created_post.slug]))
        self.assertEqual(created_post.author, self.user)
        self.assertTrue(created_post.is_published)

    def test_comment_create_adds_comment(self):
        response = self.client.post(
            reverse('comment_create', args=[self.post.slug]),
            {
                'name': 'Jan',
                'email': 'jan@example.com',
                'content': 'Bardzo dobry wpis!',
            },
        )

        self.assertRedirects(response, reverse('post_detail', args=[self.post.slug]))
        self.assertTrue(Comment.objects.filter(post=self.post, email='jan@example.com').exists())

    def test_duplicate_email_comment_is_rejected(self):
        Comment.objects.create(
            post=self.post,
            name='Jan',
            email='jan@example.com',
            content='Pierwszy komentarz',
            is_approved=True,
        )

        response = self.client.post(
            reverse('comment_create', args=[self.post.slug]),
            {
                'name': 'Jan',
                'email': 'jan@example.com',
                'content': 'Drugi komentarz',
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ten email już skomentował ten post')
        self.assertEqual(Comment.objects.filter(post=self.post, email='jan@example.com').count(), 1)

    def test_like_post_toggles_like(self):
        self.client.post(reverse('like_post', args=[self.post.slug]), REMOTE_ADDR='127.0.0.1')
        self.assertTrue(Like.objects.filter(post=self.post, ip_address='127.0.0.1').exists())

        self.client.post(reverse('like_post', args=[self.post.slug]), REMOTE_ADDR='127.0.0.1')
        self.assertFalse(Like.objects.filter(post=self.post, ip_address='127.0.0.1').exists())

    def test_author_page_renders(self):
        response = self.client.get(reverse('author_detail', args=[self.user.username]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)

    def test_author_can_edit_own_post(self):
        self.client.login(username='autor', password='Secret123')
        response = self.client.post(
            reverse('edit_post', args=[self.post.slug]),
            {
                'title': 'Pierwszy wpis po zmianie',
                'image_url': '',
                'content': 'Zmieniona tresc posta o odpowiedniej dlugosci do walidacji. ' * 2,
                'category': self.category.pk,
                'tags': [self.tag.pk],
            },
        )

        self.post.refresh_from_db()
        self.assertRedirects(response, reverse('post_detail', args=[self.post.slug]))
        self.assertEqual(self.post.title, 'Pierwszy wpis po zmianie')

    def test_other_user_cannot_edit_foreign_post(self):
        other_user = User.objects.create_user(
            username='inna',
            email='inna@example.com',
            password='Secret123',
        )
        self.client.login(username='inna', password='Secret123')

        response = self.client.get(reverse('edit_post', args=[self.post.slug]))

        self.assertEqual(response.status_code, 404)

    def test_author_can_delete_own_post(self):
        self.client.login(username='autor', password='Secret123')

        response = self.client.post(reverse('delete_post', args=[self.post.slug]))

        self.assertRedirects(response, reverse('my_posts'))
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())

    def test_my_posts_filters_by_query_and_featured(self):
        self.client.login(username='autor', password='Secret123')
        Post.objects.create(
            title='Drugi wpis testowy',
            content='Kolejna dluga tresc posta wykorzystywana do testow. ' * 3,
            category=self.category,
            author=self.user,
            is_published=True,
            is_featured=True,
        )

        response = self.client.get(reverse('my_posts'), {'q': 'Drugi', 'featured': '1'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Drugi wpis testowy')
        self.assertNotContains(response, 'Pierwszy wpis')

    def test_author_can_toggle_comment_visibility_for_own_post(self):
        comment = Comment.objects.create(
            post=self.post,
            name='Jan',
            email='jan2@example.com',
            content='Komentarz do ukrycia',
            is_approved=True,
        )
        self.client.login(username='autor', password='Secret123')

        response = self.client.post(reverse('toggle_comment_approval', args=[comment.pk]))

        comment.refresh_from_db()
        self.assertRedirects(response, reverse('my_comments'))
        self.assertFalse(comment.is_approved)

    def test_author_can_delete_comment_from_own_post(self):
        comment = Comment.objects.create(
            post=self.post,
            name='Jan',
            email='jan3@example.com',
            content='Komentarz do usuniecia',
            is_approved=True,
        )
        self.client.login(username='autor', password='Secret123')

        response = self.client.post(reverse('delete_comment', args=[comment.pk]))

        self.assertRedirects(response, reverse('my_comments'))
        self.assertFalse(Comment.objects.filter(pk=comment.pk).exists())

    def test_my_comments_page_renders_author_comments(self):
        Comment.objects.create(
            post=self.post,
            name='Jan',
            email='jan4@example.com',
            content='Komentarz widoczny w panelu',
            is_approved=False,
        )
        self.client.login(username='autor', password='Secret123')

        response = self.client.get(reverse('my_comments'), {'status': 'hidden'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Komentarz widoczny w panelu')
