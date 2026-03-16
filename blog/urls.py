from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('kontakt/', views.contact, name='contact'),
    path('author/<str:username>/', views.author_detail, name='author_detail'),
    path('my-comments/', views.my_comments, name='my_comments'),
    path('my-posts/', views.my_posts, name='my_posts'),
    path('post/create/', views.create_post, name='create_post'),
    path('post/<slug>/edit/', views.edit_post, name='edit_post'),
    path('post/<slug>/delete/', views.delete_post, name='delete_post'),
    path('comments/<int:pk>/toggle/', views.toggle_comment_approval, name='toggle_comment_approval'),
    path('comments/<int:pk>/delete/', views.delete_comment, name='delete_comment'),
    path('post/<slug>/', views.post_detail, name='post_detail'),
    path('post/<slug>/like/', views.like_post, name='like_post'),
    path('post/<slug>/comment/', views.comment_create, name='comment_create'),
    path('category/<slug>/', views.category_detail, name='category_detail'),
    path('tag/<slug>/', views.tag_detail, name='tag_detail'),
    path('search/', views.search, name='search'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
]
