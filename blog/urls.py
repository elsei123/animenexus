from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = 'Animenexus'

urlpatterns = [
    # Home and post browsing
    path('', views.post_list, name='post_list'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/new/', views.create_post, name='create_post'),
    path('post/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path("", views.post_list,     name="post_list"),

    # Comments management
    path('comment/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),

    # User actions
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),

    # Static pages
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    path('login/',
         auth_views.LoginView.as_view(template_name='registration/login.html'),
         name='login'),
    path('logout/',
         auth_views.LogoutView.as_view(next_page='Animenexus:post_list'),
         name='logout'),
]
