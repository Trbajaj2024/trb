from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Announcement, Event

@receiver([post_save, post_delete], sender=Announcement)
def clear_announcements_cache(sender, **kwargs):
    cache.delete('home_announcements')

@receiver(post_save, sender=Event)
def create_event_notification(sender, instance, created, **kwargs):
    if created:
        # Send notification to admins about new event
        pass 