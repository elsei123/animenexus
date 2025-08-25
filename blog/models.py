from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Category(models.Model):
    """
    Model representing a blog post category.
    """

    name = models.CharField(
        max_length=255,
        unique=True,
        help_text="Name of the category."
    )
    description = models.TextField(
        blank=True,
        help_text="Optional description of the category."
    )

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
        ]

    def __str__(self) -> str:
        return self.name


class Post(models.Model):
    """
    Model representing a blog post.
    """

    title = models.CharField(max_length=200, help_text="Title of the post.")
    content = models.TextField(help_text="Content of the post.")
    cover_image = models.ImageField(
        upload_to="covers/",
        blank=True,
        null=True,
        help_text="Optional cover image."
    )

    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Timestamp when the post was created."
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="Timestamp when the post was last updated."
    )
    published_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="If set, indicates when the post was published."
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="authored_posts",
        help_text="Author of the post."
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts",
        help_text="Optional category for this post."
    )

    featured = models.BooleanField(
        default=False,
        help_text="Mark post as featured to pin on top."
    )

    class Meta:
        ordering = ["-featured", "-created_at"]
        indexes = [
            models.Index(fields=["-created_at"]),
            models.Index(fields=["featured"]),
        ]

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"post_id": self.id})

    def publish(self):
        """
        Mark the post as published by updating its timestamp.
        """
        if self.published_at is None:
            self.published_at = timezone.now()
            self.save(update_fields=["published_at"])


class Comment(models.Model):
    """
    Model representing a user comment on a blog post.
    """

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
        help_text="Post that this comment belongs to."
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
        help_text="User who wrote the comment."
    )
    body = models.TextField(help_text="Text content of the comment.")
    approved = models.BooleanField(
        default=False,
        help_text="Whether the comment is approved for public display."
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        help_text="Timestamp when the comment was created."
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the comment was last updated."
    )

    class Meta:

        verbose_name = "comment"
        verbose_name_plural = "comments"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["created_at"]),
        ]

    def __str__(self) -> str:
        return f'Comment by {self.user.username} on "{self.post.title}"'


class Profile(models.Model):
    """
    Extended user profile model.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
        help_text="User account this profile belongs to."
    )
    date_of_birth = models.DateField(
        null=True,
        blank=True,
        help_text="User's date of birth."
    )
    bio = models.TextField(
        blank=True,
        help_text="Short biography of the user."
    )

    class Meta:
        verbose_name = "profile"
        verbose_name_plural = "profiles"
        ordering = ["user__username"]

    def __str__(self) -> str:
        return f"Profile of {self.user.username}"

    def get_absolute_url(self):
        return reverse("profile", kwargs={"username": self.user.username})
