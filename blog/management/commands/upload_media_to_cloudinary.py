import os

import cloudinary
import cloudinary.uploader
from django.conf import settings
from django.core.management.base import BaseCommand

from blog.models import Post


class Command(BaseCommand):
    help = "Uploads local images in 'media/posts/' to Cloudinary and updates Post model references."

    def handle(self, *args, **options):
        # Configure Cloudinary using environment variables
        cloudinary.config(
            cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
            api_key=os.getenv("CLOUDINARY_API_KEY"),
            api_secret=os.getenv("CLOUDINARY_API_SECRET"),
            secure=True,
        )

        # Define the local media directory
        media_dir = os.path.join(settings.BASE_DIR, "media")
        folder_to_scan = os.path.join(media_dir, "posts")

        for root, _dirs, files in os.walk(folder_to_scan):
            for filename in files:
                local_path = os.path.join(root, filename)

                self.stdout.write(f"Uploading {filename} ...")
                try:
                    result = cloudinary.uploader.upload(local_path)
                    url = result.get("secure_url")

                    # Update the Post model with the new Cloudinary URL
                    posts = Post.objects.filter(cover_image=f"posts/{filename}")

                    for post in posts:
                        post.cover_image = url
                        post.save()
                        self.stdout.write(f"Updated Post {post.id} to use Cloudinary URL: {url}")

                except Exception as e:
                    self.stderr.write(f"Error uploading {filename}: {str(e)}")

        self.stdout.write(self.style.SUCCESS("All files processed!"))
