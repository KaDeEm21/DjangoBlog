from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Kategoria'
        verbose_name_plural = 'Kategorie'
        ordering = ['name']

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tagi'
        ordering = ['name']

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='posts',
        null=True,
        blank=True,
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()
    image_url = models.URLField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts', null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posty'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        base_slug = slugify(self.slug or self.title)
        if not base_slug:
            base_slug = 'post'

        if not self.slug:
            self.slug = base_slug

        similar_slugs = Post.objects.filter(slug__startswith=base_slug).exclude(pk=self.pk)
        if similar_slugs.filter(slug=self.slug).exists():
            suffix = 2
            while similar_slugs.filter(slug=f'{base_slug}-{suffix}').exists():
                suffix += 1
            self.slug = f'{base_slug}-{suffix}'

        super().save(*args, **kwargs)

    @property
    def reading_time(self):
        words_per_minute = 200
        word_count = len(self.content.split())
        return max(1, round(word_count / words_per_minute))


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Komentarz'
        verbose_name_plural = 'Komentarze'
        ordering = ['created_at']

    def __str__(self):
        return f'Komentarz od {self.name} do {self.post.title}'


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    ip_address = models.GenericIPAddressField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Polubienie'
        verbose_name_plural = 'Polubienia'
        unique_together = ['post', 'ip_address']
        ordering = ['-created_at']

    def __str__(self):
        return f'Like for {self.post.title}'


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    avatar = models.URLField(blank=True)
    bio = models.TextField(blank=True)
    website = models.URLField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Profil użytkownika'
        verbose_name_plural = 'Profile użytkowników'

    def __str__(self):
        return f'{self.user.username}'


@receiver(post_save, sender=get_user_model())
def ensure_profile_exists(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        return

    Profile.objects.get_or_create(user=instance)
