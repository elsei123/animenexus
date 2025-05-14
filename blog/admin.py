from django.contrib import admin
from .models import Category, Post, Comment, Profile


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin view for blog categories."""
    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Admin view for blog posts."""
    list_display = ("title", "author", "category", "created_at")
    search_fields = ("title", "content")
    list_filter = ("author", "category", "created_at")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin view for blog comments."""
    list_display = ("post", "user", "body", "approved", "created_at")
    list_filter = ("approved", "created_at")
    search_fields = ("body", "user__username")
    ordering = ("-created_at",)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Admin view for user profiles."""
    list_display = ("user", "date_of_birth")
    search_fields = ("user__username",)
