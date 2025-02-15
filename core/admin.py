from django.contrib import admin
from django.utils.html import format_html
from .models import *

class SEOModelAdmin(admin.ModelAdmin):
    """Base admin class for models with SEO fields"""
    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        seo_fields = (
            'SEO', {
                'fields': ('meta_title', 'meta_description', 'meta_keywords'),
                'classes': ('collapse',)
            }
        )
        return fieldsets + (seo_fields,)

@admin.register(SchoolInfo)
class SchoolInfoAdmin(SEOModelAdmin):
    list_display = ('name', 'email', 'phone', 'last_updated')
    readonly_fields = ('last_updated',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'logo', 'address', 'email', 'phone')
        }),
        ('Content', {
            'fields': ('mission_statement', 'vision')
        }),
    )

@admin.register(Event)
class EventAdmin(SEOModelAdmin):
    list_display = ('title', 'event_type', 'start_datetime', 'location', 'is_registration_open', 'registered_count')
    list_filter = ('event_type', 'registration_required')
    search_fields = ('title', 'description', 'location')
    date_hierarchy = 'start_datetime'
    
    def registered_count(self, obj):
        return obj.get_registered_count()
    registered_count.short_description = 'Registrations'

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_posted', 'is_active', 'preview_image')
    list_filter = ('is_active', 'date_posted')
    search_fields = ('title', 'content')
    
    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px;" />', obj.image.url)
        return '-'
    preview_image.short_description = 'Image'

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'email', 'preview_photo')
    list_filter = ('role',)
    search_fields = ('name', 'email', 'bio')
    
    def preview_photo(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="max-height: 50px;" />', obj.photo.url)
        return '-'
    preview_photo.short_description = 'Photo'

# Add more admin configurations... 