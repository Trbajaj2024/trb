from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Public pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms/', views.terms, name='terms'),
    
    # Academic pages
    path('academics/', views.academics, name='academics'),
    path('courses/<slug:slug>/', views.course_detail, name='course_detail'),
    path('faculty/', views.faculty_list, name='faculty_list'),
    
    # News and Events
    path('news/', views.news_list, name='news_list'),
    path('news/<slug:slug>/', views.news_detail, name='news_detail'),
    path('events/', views.event_list, name='event_list'),
    path('events/<slug:slug>/', views.event_detail, name='event_detail'),
    
    # Parent Portal
    path('parents/', views.parents_dashboard, name='parents_dashboard'),
    path('parents/messages/', views.parent_messages, name='parent_messages'),
    path('parents/payments/', views.parent_payments, name='parent_payments'),
    
    # API endpoints
    path('api/newsletter-signup/', views.newsletter_signup, name='newsletter_signup'),
    path('api/contact-form/', views.contact_form_submit, name='contact_form_submit'),
] 