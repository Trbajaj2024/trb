from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def meta_tags(obj=None):
    meta = []
    
    if obj:
        meta.append(f'<title>{obj.get_meta_title()}</title>')
        meta.append(f'<meta name="description" content="{obj.get_meta_description()}">')
        if obj.meta_keywords:
            meta.append(f'<meta name="keywords" content="{obj.meta_keywords}">')
    
    # Open Graph tags
    if hasattr(obj, 'image') and obj.image:
        meta.append(f'<meta property="og:image" content="{obj.image.url}">')
    
    return mark_safe('\n'.join(meta)) 