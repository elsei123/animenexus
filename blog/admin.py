from django.contrib import admin
from django.utils.html import format_html

from .models import Category, Comment, Post, Profile


def make_public(modeladmin, request, queryset):
    """Custom action to mark selected posts as featured."""
    queryset.update(featured=True)
    make_public.short_description = "Mark selected posts as featured"


def make_unpublic(modeladmin, request, queryset):
    """Custom action to unmark selected posts as featured."""
    queryset.update(featured=False)
    make_unpublic.short_description = "Unmark selected posts as featured"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin view for blog categories."""

    list_display = ("name", "description")
    search_fields = ("name",)
    list_per_page = 20


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Admin view for blog posts."""

    list_display = (
        "title",
        "author_link",
        "category",
        "created_at",
        "featured",
    )
    list_editable = ("featured",)
    list_filter = ("author", "category", "featured", "created_at")
    search_fields = ("title", "content", "author__username")
    date_hierarchy = "created_at"
    raw_id_fields = ("author", "category")
    actions = (make_public, make_unpublic)

    def author_link(self, obj):
        return format_html(
            '<a href="{}">{}</a>', obj.author.profile.get_absolute_url(),
            obj.author.username
        )

    author_link.short_description = "Author"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin view for blog comments."""

    list_display = ("post_link", "user_link", "short_body", "approved", "created_at")
    list_filter = ("approved", "created_at")
    list_editable = ("approved",)
    search_fields = ("body", "user__username", "post__title")
    raw_id_fields = ("post", "user")
    date_hierarchy = "created_at"

    def short_body(self, obj):
        return (obj.body[:75] + "...") if len(obj.body) > 75 else obj.body

    short_body.short_description = "Comment"

    def post_link(self, obj):
        url = obj.post.get_absolute_url()
        return format_html('<a href="{}">{}</a>', url, obj.post.title)

    post_link.short_description = "Post"

    def user_link(self, obj):
        url = obj.user.profile.get_absolute_url()
        return format_html('<a href="{}">{}</a>', url, obj.user.username)

    user_link.short_description = "User"


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Admin view for user profiles."""

    list_display = ("user_link", "date_of_birth")
    search_fields = ("user__username", "user__email")
    list_filter = ("date_of_birth",)
    raw_id_fields = ("user",)
    date_hierarchy = "date_of_birth"

    def user_link(self, obj):
        return format_html(
            '<a href="{}">{}</a>', obj.get_absolute_url(),
            obj.user.username
        )

    user_link.short_description = "User"
