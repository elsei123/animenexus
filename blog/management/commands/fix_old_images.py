import os
import cloudinary.uploader
from django.core.management.base import BaseCommand
from django.conf import settings
from blog.models import Post


class Command(BaseCommand):
    help = "Reupload old Post.cover_image files from local /media to Cloudinary"

    def handle(self, *args, **options):
        fixed = 0
        skipped = 0

        for post in Post.objects.exclude(cover_image="").all():
            path = str(post.cover_image)

            if path.startswith("http") or "cloudinary.com" in path:
                skipped += 1
                continue

            local_path = os.path.join(settings.MEDIA_ROOT, path)
            if not os.path.exists(local_path):
                self.stdout.write(f"⚠️ File not found for Post {post.id}: {local_path}")
                skipped += 1
                continue

            try:
                result = cloudinary.uploader.upload(
                    local_path,
                    folder="covers",
                    use_filename=True,
                    unique_filename=False,
                )
                post.cover_image = result["secure_url"]
                post.save(update_fields=["cover_image"])
                fixed += 1
                self.stdout.write(f"✅ Fixed Post {post.id} → {result['secure_url']}")
            except Exception as e:
                self.stderr.write(f"❌ Error uploading {local_path}: {e}")
                skipped += 1

        self.stdout.write(self.style.SUCCESS(
            f"Done! Fixed {fixed} posts, skipped {skipped}."
        ))
