from django import template

register = template.Library()

@register.inclusion_tag('includes/pagination.html')
def show_pagination(page_obj, extra_params=''):
    return {
        'page_obj': page_obj,
        'extra_params': extra_params
    } 