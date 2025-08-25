from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    # Home
    path("", views.post_list, name="post_list"),

    # Posts
    path("post/<int:post_id>/", views.post_detail, name="post_detail"),
    path("post/create/", views.create_post, name="create_post"),
    path("post/<int:post_id>/edit/", views.edit_post, name="edit_post"),
    path("post/<int:post_id>/delete/", views.delete_post, name="delete_post"),

    # Comments
    path("comment/<int:comment_id>/edit/", views.edit_comment, name="edit_comment"),
    path("comment/<int:comment_id>/delete/",
         views.delete_comment, name="delete_comment"),

    # Static/info
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),

    # Auth/profile
    path("signup/", views.signup, name="signup"),
    path("profile/<str:username>/", views.profile, name="profile"),
]
