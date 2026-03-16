from django.contrib import admin
from .models import Category, Tag, Post, Comment, Like, Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'website', 'location', 'created_at']
    search_fields = ['user__username', 'bio']
    readonly_fields = ['created_at']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'name', 'created_at', 'is_approved']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['name', 'content']
    readonly_fields = ['post', 'name', 'email', 'content', 'created_at']
    raw_id_fields = ['post']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'created_at', 'is_published', 'is_featured', 'likes_count', 'comments_count']
    search_fields = ['title', 'content', 'author__username']
    list_filter = ['category', 'is_published', 'is_featured', 'created_at']
    filter_horizontal = ['tags']
    readonly_fields = ['created_at', 'updated_at', 'reading_time']

    def likes_count(self, obj):
        return obj.likes.count()
    likes_count.short_description = 'Liczba polubień'

    def comments_count(self, obj):
        return obj.comments.filter(is_approved=True).count()
    comments_count.short_description = 'Liczba komentarzy'

    def reading_time(self, obj):
        return f"{obj.reading_time} min"
    reading_time.short_description = 'Czas czytania'


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['post', 'ip_address', 'created_at']
    list_filter = ['created_at']
    readonly_fields = ['post', 'ip_address', 'created_at']
