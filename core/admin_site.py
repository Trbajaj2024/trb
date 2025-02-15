from django.contrib.admin import AdminSite
from django.template.response import TemplateResponse
from django.urls import path

class SchoolAdminSite(AdminSite):
    site_header = 'School Administration'
    site_title = 'School Admin Portal'
    index_title = 'Welcome to School Admin Portal'
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('analytics/', self.admin_view(self.analytics_view), name='analytics'),
        ]
        return custom_urls + urls
    
    def analytics_view(self, request):
        context = {
            **self.each_context(request),
            'title': 'Site Analytics'
        }
        return TemplateResponse(request, "admin/analytics.html", context)

admin_site = SchoolAdminSite(name='school_admin') 