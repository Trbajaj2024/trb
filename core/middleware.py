from django.middleware.security import SecurityMiddleware
from django.http import HttpResponseRedirect
from django.conf import settings
import re

class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Security Headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response['Permissions-Policy'] = 'geolocation=(), microphone=()'
        
        if settings.DEBUG:
            return response
            
        # Add HSTS header in production
        response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        return response

class AdminIPRestrictionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.allowed_ips = settings.ADMIN_ALLOWED_IPS

    def __call__(self, request):
        if request.path.startswith('/admin/'):
            ip = self.get_client_ip(request)
            if ip not in self.allowed_ips:
                return HttpResponseRedirect('/')
        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR') 