from django.contrib.sitemaps import Sitemap
from .models import Event, Announcement

class EventSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.7

    def items(self):
        return Event.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at

class AnnouncementSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return Announcement.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.date_posted 