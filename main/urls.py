from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('academics/', views.academics, name='academics'),
    path('admissions/', views.admissions, name='admissions'),
    path('contact/', views.contact, name='contact'),
    path('facilities/', views.facilities, name='facilities'),
    path('events/', views.events, name='events'),
    path('student/signup/', views.student_signup, name='student_signup'),
    path('teacher/signup/', views.teacher_signup, name='teacher_signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('live-classes/', views.live_classes, name='live_classes'),
    path('test-email/', views.test_email, name='test_email'),
    path('courses/', views.courses, name='courses'),
    path('courses/<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('subjects/<int:subject_id>/', views.subject_detail, name='subject_detail'),
    path('get-video-url/<int:chapter_id>/', views.get_video_url, name='get_video_url'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
] 