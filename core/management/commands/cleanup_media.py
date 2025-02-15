from django.core.management.base import BaseCommand
from django.core.files.storage import default_storage
from core.models import Event, Announcement
import os

class Command(BaseCommand):
    help = 'Clean up unused media files'

    def handle(self, *args, **options):
        # Get all media files in use
        used_files = set()
        for model in [Event, Announcement]:
            for obj in model.objects.all():
                if obj.image:
                    used_files.add(obj.image.name)

        # Check all files in media directory
        for root, dirs, files in os.walk(settings.MEDIA_ROOT):
            for filename in files:
                filepath = os.path.join(root, filename)
                relative_path = os.path.relpath(filepath, settings.MEDIA_ROOT)
                if relative_path not in used_files:
                    os.remove(filepath)
                    self.stdout.write(f'Removed unused file: {relative_path}') 