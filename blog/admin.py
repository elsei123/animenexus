from django.contrib import admin
from django.utils.html import format_html

from .models import Category, Comment, Post, Profile


@admin.action(description="Mark selected posts as featured")
def mark_featured(modeladmin, request, queryset):
    queryset.update(featured=True)


@admin.action(description="Unmark selected posts as featured")
def unmark_featured(modeladmin, request, queryset):
    queryset.update(featured=False)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin view for blog categories."""

    list_display = ("name", "description")
    search_fields = ("name",)
    list_per_page = 20
    empty_value_display = "—"


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
    list_select_related = ("author", "category")
    empty_value_display = "—"

    @admin.display(description="Author", ordering="author__username")
    def author_link(self, obj):
        # Try link to frontend profile if exists, else admin user change
        profile = getattr(obj.author, "profile", None)
        if profile:
            return format_html('<a href="{}">{}</a>', profile.get_absolute_url(), obj.author.username)
        user_admin_url = reverse("admin:auth_user_change", args=[obj.author.id])
        return format_html('<a href="{}">{}</a>', user_admin_url, obj.author.username)


# -------- Actions (Comments) --------
@admin.action(description="Approve selected comments")
def approve_comments(modeladmin, request, queryset):
    queryset.update(approved=True)


@admin.action(description="Unapprove selected comments")
def unapprove_comments(modeladmin, request, queryset):
    queryset.update(approved=False)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin view for blog comments."""

    list_display = ("post_link", "user_link", "short_body", "approved", "created_at")
    list_filter = ("approved", "created_at")
    list_editable = ("approved",)
    search_fields = ("body", "user__username", "post__title")
    autocomplete_fields = ("post", "user")
    date_hierarchy = "created_at"
    actions = (approve_comments, unapprove_comments)
    list_select_related = ("post", "user")
    empty_value_display = "—"

    @admin.display(description="Comment")
    def short_body(self, obj):
        body = obj.body or ""
        return (body[:75] + "...") if len(body) > 75 else body

    @admin.display(description="Post", ordering="post__title")
    def post_link(self, obj):
        url = obj.post.get_absolute_url()
        return format_html('<a href="{}">{}</a>', url, obj.post.title)

    @admin.display(description="User", ordering="user__username")
    def user_link(self, obj):
        profile = getattr(obj.user, "profile", None)
        if profile:
           return format_html('<a href="{}">{}</a>', profile.get_absolute_url(), obj.user.username)
        user_admin_url = reverse("admin:auth_user_change", args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', user_admin_url, obj.user.username)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Admin view for user profiles."""

    list_display = ("user_link", "date_of_birth")
    search_fields = ("user__username", "user__email")
    list_filter = ("date_of_birth",)
    autocomplete_fields = ("user",)
    date_hierarchy = "date_of_birth"
    empty_value_display = "—"

    @admin.display(description="User", ordering="user__username")
    def user_link(self, obj):
        return format_html('<a href="{}">{}</a>', obj.get_absolute_url(), obj.user.username)
