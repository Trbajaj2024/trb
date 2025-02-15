from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    User, Student, Teacher, Carousel, Statistic, 
    Program, Event, Testimonial, Achievement, Notice, 
    ContactMessage, LiveClass, Course, Subject, Chapter, VideoLecture,
    AboutPage, Feature, TimelineEvent, CoreValue, 
    CallToAction
)
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
import csv
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse

# Custom admin site
class SchoolAdminSite(admin.AdminSite):
    site_header = 'Taradevi RameshwarLal Bajaj School Administration'
    site_title = 'TRBSS Admin Portal'
    index_title = 'School Administration'

    def each_context(self, request):
        context = super().each_context(request)
        context['css_files'] = [
            'admin/css/custom_admin.css',
        ]
        return context

admin_site = SchoolAdminSite(name='school_admin')

# 1. User Management
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_student', 'is_teacher', 'is_staff')
    list_filter = ('is_student', 'is_teacher', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('User Type', {'fields': ('is_student', 'is_teacher')}),
    )

class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'roll_number', 'grade', 'section', 'parent_name')
    search_fields = ('user__username', 'roll_number', 'parent_name')
    list_filter = ('grade', 'section')
    change_list_template = 'admin/student_changelist.html'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-csv/', self.import_csv, name='student-import-csv'),
            path('download-template/', self.download_template, name='download-student-template'),
        ]
        return custom_urls + urls

    def import_csv(self, request):
        if request.method == 'POST':
            csv_file = request.FILES.get('csv_file')
            if csv_file:
                try:
                    decoded_file = csv_file.read().decode('utf-8').splitlines()
                    reader = csv.DictReader(decoded_file)
                    for row in reader:
                        user = User.objects.create(
                            username=row['username'],
                            email=row['email'],
                            password=make_password(row['password']),
                            first_name=row['first_name'],
                            last_name=row['last_name'],
                            phone=row['phone'],
                            address=row['address'],
                            is_student=True
                        )
                        Student.objects.create(
                            user=user,
                            roll_number=row['roll_number'],
                            grade=row['grade'],
                            section=row['section'],
                            parent_name=row['parent_name'],
                            parent_phone=row['parent_phone']
                        )
                    messages.success(request, 'Students imported successfully')
                except Exception as e:
                    messages.error(request, f'Error importing students: {str(e)}')
            return redirect('..')
        return render(request, 'admin/csv_form.html')

    def download_template(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="student_template.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'username', 'email', 'password', 'first_name', 'last_name',
            'roll_number', 'grade', 'section', 'parent_name', 'parent_phone',
            'phone', 'address'
        ])
        # Add sample data
        writer.writerow([
            'john_doe', 'john@example.com', 'securepass123', 'John', 'Doe',
            'R2023001', '10', 'A', 'James Doe', '9876543210',
            '1234567890', '123 Main St'
        ])
        return response

class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'employee_id', 'subject', 'qualification')
    search_fields = ('user__username', 'employee_id', 'subject')
    list_filter = ('subject',)
    change_list_template = 'admin/teacher_changelist.html'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-csv/', self.import_csv, name='teacher-import-csv'),
            path('download-template/', self.download_template, name='download-teacher-template'),
        ]
        return custom_urls + urls

    def import_csv(self, request):
        if request.method == 'POST':
            csv_file = request.FILES.get('csv_file')
            if csv_file:
                try:
                    decoded_file = csv_file.read().decode('utf-8').splitlines()
                    reader = csv.DictReader(decoded_file)
                    for row in reader:
                        user = User.objects.create(
                            username=row['username'],
                            email=row['email'],
                            password=make_password(row['password']),
                            first_name=row['first_name'],
                            last_name=row['last_name'],
                            phone=row['phone'],
                            address=row['address'],
                            is_teacher=True
                        )
                        Teacher.objects.create(
                            user=user,
                            employee_id=row['employee_id'],
                            subject=row['subject'],
                            qualification=row['qualification']
                        )
                    messages.success(request, 'Teachers imported successfully')
                except Exception as e:
                    messages.error(request, f'Error importing teachers: {str(e)}')
            return redirect('..')
        return render(request, 'admin/csv_form.html')

    def download_template(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="teacher_template.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'username', 'email', 'password', 'first_name', 'last_name',
            'employee_id', 'subject', 'qualification', 'phone', 'address'
        ])
        # Add sample data
        writer.writerow([
            'prof_brown', 'brown@example.com', 'securepass123', 'Robert', 'Brown',
            'EMP001', 'Mathematics', 'Ph.D. in Mathematics', '9876543213', '321 Elm St'
        ])
        return response

# 2. Course Management
class VideoLectureInline(admin.TabularInline):
    model = VideoLecture
    extra = 1

class ChapterInline(admin.TabularInline):
    model = Chapter
    extra = 1

class SubjectInline(admin.TabularInline):
    model = Subject
    extra = 1

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'image', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    inlines = [SubjectInline]

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
    search_fields = ('title', 'course__title')
    inlines = [ChapterInline]

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'order')
    list_filter = ('subject__course', 'subject')
    search_fields = ('title', 'subject__title')
    inlines = [VideoLectureInline]

@admin.register(VideoLecture)
class VideoLectureAdmin(admin.ModelAdmin):
    list_display = ('title', 'chapter', 'video_id', 'order', 'duration')
    list_filter = ('chapter__subject__course', 'chapter__subject', 'chapter')
    search_fields = ('title', 'video_id')

# 3. Content Management
@admin.register(Carousel)
class CarouselAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'is_active', 'for_students', 'for_teachers')
    list_editable = ('is_active', 'for_students', 'for_teachers')
    list_filter = ('is_active', 'for_students', 'for_teachers', 'date')
    search_fields = ('title', 'content')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'is_featured', 'is_active')
    list_editable = ('is_featured', 'is_active')
    list_filter = ('is_featured', 'is_active', 'date')
    search_fields = ('title', 'description')

# 4. Live Classes
@admin.register(LiveClass)
class LiveClassAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'platform', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('platform', 'is_active', 'date')
    search_fields = ('title', 'description')

# 5. Communication
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at',)

# Register models with categories
# 1. User Management
admin_site.register(User, CustomUserAdmin)
admin_site.register(Student, StudentAdmin)
admin_site.register(Teacher, TeacherAdmin)

# 2. Course Management
admin_site.register(Course, CourseAdmin)
admin_site.register(Subject, SubjectAdmin)
admin_site.register(Chapter, ChapterAdmin)
admin_site.register(VideoLecture, VideoLectureAdmin)

# 3. Content Management
admin_site.register(Carousel, CarouselAdmin)
admin_site.register(Notice, NoticeAdmin)
admin_site.register(Event, EventAdmin)

# 4. Live Classes
admin_site.register(LiveClass, LiveClassAdmin)

# 5. Communication
admin_site.register(ContactMessage, ContactMessageAdmin)

@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    list_display = ('hero_title', 'hero_subtitle')
    fieldsets = (
        ('Hero Section', {
            'fields': ('hero_title', 'hero_subtitle', 'hero_image')
        }),
        ('Welcome Section', {
            'fields': ('welcome_title', 'welcome_description', 'welcome_image')
        }),
    )

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'description')

@admin.register(TimelineEvent)
class TimelineEventAdmin(admin.ModelAdmin):
    list_display = ('year', 'title', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('year', 'title', 'description')

@admin.register(CoreValue)
class CoreValueAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'description')

@admin.register(CallToAction)
class CallToActionAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'is_active')
    list_editable = ('is_active',)
    search_fields = ('title', 'subtitle')