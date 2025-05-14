from django.conf import settings
from django.db import models
from django.utils import timezone


class Category(models.Model):
    """
    Model representing a blog post category.
    """
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Post(models.Model):
    """
    Model representing a blog post.
    """
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts"
    )
    cover_image = models.ImageField(
        upload_to="posts/",
        blank=True,
        null=True,
        help_text="Optional cover image for the post."
    )
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "post"
        verbose_name_plural = "posts"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Comment(models.Model):
    """
    Model representing a user comment on a blog post.
    """
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    body = models.TextField()
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "comment"
        verbose_name_plural = "comments"
        ordering = ["-created_at"]

    def __str__(self):
        return f'Comment by {self.user.username} on "{self.post.title}"'


class Profile(models.Model):
    """
    Extended user profile model.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    date_of_birth = models.DateField(
        null=True,
        blank=True,
        help_text="User's date of birth."
    )

    class Meta:
        verbose_name = "profile"
        verbose_name_plural = "profiles"

    def __str__(self):
        return f"Profile of {self.user.username}"
