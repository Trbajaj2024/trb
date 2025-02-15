from .models import SchoolInfo, SocialMedia

def school_context(request):
    """Add school info and social media links to all templates"""
    return {
        'school_info': SchoolInfo.objects.first(),
        'social_media': SocialMedia.objects.filter(is_active=True),
    } 