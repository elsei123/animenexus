"""
URL configuration for animenexus project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from blog import views as blog_views

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", blog_views.post_list, name="post_list"),
    path("post/<int:post_id>/", blog_views.post_detail, name="post_detail"),
    path("post/create/", blog_views.create_post, name="create_post"),
    path("post/<int:post_id>/edit/", blog_views.edit_post, name="edit_post"),
    path("post/<int:post_id>/delete/", blog_views.delete_post, name="delete_post"),

    path("comment/<int:comment_id>/edit/",
         blog_views.edit_comment, name="edit_comment"),
    path("comment/<int:comment_id>/delete/",
         blog_views.delete_comment, name="delete_comment"),

    path("about/", blog_views.about, name="about"),
    path("contact/", blog_views.contact, name="contact"),

    path("signup/", blog_views.signup, name="signup"),
    path("profile/", blog_views.profile, name="profile"),
    path("profile/<str:username>/", blog_views.profile, name="profile"),
    path("accounts/", include("django.contrib.auth.urls")),
    # path("", include("blog.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
