from django.core.management.base import BaseCommand
from blog.models import Post


class Command(BaseCommand):
    help = "Fix Post.cover_image paths to remove invalid 'media/' prefix for Cloudinary."

    def handle(self, *args, **kwargs):
        fixed_count = 0

        for post in Post.objects.exclude(cover_image="").all():
            if post.cover_image.name.startswith("media/covers/"):
                old_path = post.cover_image.name
                new_path = old_path.replace("media/", "", 1)
                post.cover_image.name = new_path
                post.save(update_fields=["cover_image"])
                self.stdout.write(f"✔ Updated {old_path} -> {new_path}")
                fixed_count += 1

        if fixed_count:
            self.stdout.write(
                self.style.SUCCESS(f"Fixed {fixed_count} Post.cover_image paths.")
            )
        else:
            self.stdout.write("No posts needed fixing.")
