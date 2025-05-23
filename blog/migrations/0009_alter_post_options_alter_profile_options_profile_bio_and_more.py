# Generated by Django 5.2 on 2025-05-14 21:52

import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0008_alter_category_options_alter_comment_options_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="post",
            options={"ordering": ["-featured", "-created_at"]},
        ),
        migrations.AlterModelOptions(
            name="profile",
            options={
                "ordering": ["user__username"],
                "verbose_name": "profile",
                "verbose_name_plural": "profiles",
            },
        ),
        migrations.AddField(
            model_name="profile",
            name="bio",
            field=models.TextField(
                blank=True, help_text="Short biography of the user."
            ),
        ),
        migrations.AlterField(
            model_name="category",
            name="description",
            field=models.TextField(
                blank=True, help_text="Optional description of the category."
            ),
        ),
        migrations.AlterField(
            model_name="category",
            name="name",
            field=models.CharField(
                help_text="Name of the category.", max_length=255, unique=True
            ),
        ),
        migrations.AlterField(
            model_name="comment",
            name="approved",
            field=models.BooleanField(
                default=False, help_text="Designates whether the comment is approved."
            ),
        ),
        migrations.AlterField(
            model_name="comment",
            name="body",
            field=models.TextField(help_text="Text content of the comment."),
        ),
        migrations.AlterField(
            model_name="comment",
            name="created_at",
            field=models.DateTimeField(
                default=django.utils.timezone.now,
                help_text="Timestamp when the comment was created.",
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="content",
            field=models.TextField(help_text="Content of the post."),
        ),
        migrations.AlterField(
            model_name="post",
            name="cover_image",
            field=models.ImageField(
                blank=True,
                help_text="Optional cover image for the post.",
                null=True,
                upload_to="covers/",
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, help_text="Timestamp when the post was created."
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="featured",
            field=models.BooleanField(
                default=False, help_text="Mark post as featured on the home page."
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="title",
            field=models.CharField(help_text="Title of the post.", max_length=200),
        ),
        migrations.AlterField(
            model_name="post",
            name="updated_at",
            field=models.DateTimeField(
                auto_now=True, help_text="Timestamp when the post was last updated."
            ),
        ),
        migrations.AddIndex(
            model_name="category",
            index=models.Index(fields=["name"], name="blog_catego_name_cb8828_idx"),
        ),
        migrations.AddIndex(
            model_name="comment",
            index=models.Index(
                fields=["created_at"], name="blog_commen_created_4e025c_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="post",
            index=models.Index(
                fields=["-created_at"], name="blog_post_created_45f0c6_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="post",
            index=models.Index(
                fields=["featured"], name="blog_post_feature_716fbe_idx"
            ),
        ),
    ]
