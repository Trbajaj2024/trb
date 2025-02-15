from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import StudentSignUpForm, TeacherSignUpForm
from django.utils import timezone
from .models import Carousel, Statistic, Program, Event, Testimonial, Achievement, Notice, ContactMessage, LiveClass, Course, Subject, Chapter, AboutPage, Feature, TimelineEvent, CoreValue, CallToAction, AcademicLevel, Department
from django.http import HttpResponse, JsonResponse
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView

def home(request):
    context = {
        'carousels': Carousel.objects.filter(is_active=True),
        'stats': Statistic.objects.all(),
        'featured_programs': Program.objects.filter(is_active=True),
        'upcoming_events': Event.objects.filter(
            is_active=True,
            date__gte=timezone.now()
        )[:3],
        'testimonials': Testimonial.objects.filter(is_active=True),
        'achievements': Achievement.objects.filter(is_featured=True)[:3],
        'live_classes': LiveClass.objects.filter(is_active=True)[:3],
        'courses': Course.objects.all()[:3]
    }
    return render(request, 'main/home.html', context)

def about(request):
    context = {
        'about': AboutPage.objects.first(),
        'features': Feature.objects.filter(is_active=True),
        'timeline_events': TimelineEvent.objects.filter(is_active=True),
        'core_values': CoreValue.objects.filter(is_active=True),
        'cta': CallToAction.objects.filter(location='about_page', is_active=True).first()
    }
    return render(request, 'main/about.html', context)

def academics(request):
    context = {
        'academic_levels': AcademicLevel.objects.filter(is_active=True),
        'departments': Department.objects.filter(is_active=True),
    }
    return render(request, 'main/academics.html', context)

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Save the contact message to the database
        contact_message = ContactMessage(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        contact_message.save()

        # Send email notification (optional)
        email_message = f"Name: {name}\nEmail: {email}\nMessage: {message}"
        try:
            send_mail(
                subject,
                email_message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.CONTACT_EMAIL],
                fail_silently=False,
            )
            messages.success(request, 'Your message has been sent successfully!')
        except Exception as e:
            messages.error(request, 'There was an error sending your message. Please try again later.')
        
        return redirect('contact')
    return render(request, 'main/contact.html')

def facilities(request):
    return render(request, 'main/facilities.html')

def events(request):
    return render(request, 'main/events.html')

def admissions(request):
    if request.method == 'POST':
        student_name = request.POST.get('studentName')
        dob = request.POST.get('dob')
        grade = request.POST.get('grade')
        parent_name = request.POST.get('parentName')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        
        # Send email notification
        subject = f"New Admission Application - {student_name}"
        message = f"""
        Student Name: {student_name}
        Date of Birth: {dob}
        Grade: {grade}
        Parent's Name: {parent_name}
        Email: {email}
        Phone: {phone}
        Address: {address}
        """
        
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.ADMISSIONS_EMAIL],
                fail_silently=False,
            )
            messages.success(request, 'Your application has been submitted successfully!')
        except Exception as e:
            messages.error(request, 'There was an error submitting your application. Please try again later.')
        
        return redirect('admissions')
    return render(request, 'main/admissions.html')

def student_signup(request):
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                messages.success(request, 'Account created successfully! Welcome to your dashboard.')
                return redirect('student_dashboard')
            except Exception as e:
                messages.error(request, 'An error occurred during registration. Please try again.')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = StudentSignUpForm()
    return render(request, 'registration/student_signup.html', {'form': form})

def teacher_signup(request):
    if request.method == 'POST':
        form = TeacherSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully! Welcome to your dashboard.')
            return redirect('teacher_dashboard')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = TeacherSignUpForm()
    return render(request, 'registration/teacher_signup.html', {'form': form})

@login_required
def dashboard(request):
    if request.user.is_student:
        return redirect('student_dashboard')
    elif request.user.is_teacher:
        return redirect('teacher_dashboard')
    return redirect('home')

@login_required
def student_dashboard(request):
    if not request.user.is_student:
        messages.error(request, 'You do not have access to the student dashboard.')
        return redirect('home')
    
    context = {
        'student': request.user.student,
        'notices': Notice.objects.filter(
            is_active=True,
            for_students=True
        ).order_by('-date')[:5],
        'upcoming_events': Event.objects.filter(
            is_active=True,
            date__gte=timezone.now()
        )[:3]
    }
    return render(request, 'main/student_dashboard.html', context)

@login_required
def teacher_dashboard(request):
    if not request.user.is_teacher:
        messages.error(request, 'You do not have access to the teacher dashboard.')
        return redirect('home')
    
    context = {
        'teacher': request.user.teacher,
        'notices': Notice.objects.filter(
            is_active=True,
            for_teachers=True
        ).order_by('-date')[:5],
        'upcoming_events': Event.objects.filter(
            is_active=True,
            date__gte=timezone.now()
        )[:3]
    }
    return render(request, 'main/teacher_dashboard.html', context)

def live_classes(request):
    classes = LiveClass.objects.filter(is_active=True)
    return render(request, 'main/live_classes.html', {'classes': classes})

def test_email(request):
    subject = 'Test Email'
    message = 'This is a test email.'
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            ['recipient@example.com'],  # Change to your email
            fail_silently=False,
        )
        return HttpResponse('Email sent successfully!')
    except Exception as e:
        return HttpResponse(f'Error: {e}')

def courses(request):
    courses = Course.objects.all()
    return render(request, 'main/courses.html', {'courses': courses})

class CourseDetailView(DetailView):
    model = Course
    template_name = 'main/course_detail.html'
    context_object_name = 'course'

    def get_object(self):
        course_id = self.kwargs.get('pk')
        cache_key = f'course_{course_id}'
        course = cache.get(cache_key)
        
        if course is None:
            course = super().get_object()
            cache.set(cache_key, course, timeout=3600)
        
        return course

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        
        # Get cached subjects and their related data
        subjects = course.get_cached_subjects()
        
        for subject in subjects:
            subject.cached_chapters = subject.get_cached_chapters()
            for chapter in subject.cached_chapters:
                chapter.cached_lectures = chapter.get_cached_lectures()
        
        context['subjects'] = subjects
        return context

# Cache the course list view for 15 minutes
@method_decorator(cache_page(60 * 15), name='dispatch')
class CourseListView(ListView):
    model = Course
    template_name = 'main/courses.html'
    context_object_name = 'courses'

def subject_detail(request, subject_id):
    try:
        subject = Subject.objects.get(id=subject_id)
        chapters = subject.chapters.all()
        print(chapters)  # Debugging line
        return render(request, 'main/subject_detail.html', {'subject': subject, 'chapters': chapters})
    except Subject.DoesNotExist:
        messages.error(request, 'Subject not found.')
        return redirect('courses')

def get_video_url(request, chapter_id):
    try:
        chapter = Chapter.objects.get(id=chapter_id)
        video = chapter.video_lectures.first()
        if video:
            # Ensure the URL is in the correct format
            video_url = video.video_url
            if 'youtube.com/embed/' not in video_url:
                # If somehow the URL isn't in embed format, convert it
                if 'youtube.com/watch?v=' in video_url:
                    video_id = video_url.split('watch?v=')[1].split('&')[0]
                    video_url = f'https://www.youtube.com/embed/{video_id}'
                elif 'youtu.be/' in video_url:
                    video_id = video_url.split('youtu.be/')[1].split('?')[0]
                    video_url = f'https://www.youtube.com/embed/{video_id}'
            return JsonResponse({'video_url': video_url})
        return JsonResponse({'error': 'No video found'}, status=404)
    except Chapter.DoesNotExist:
        return JsonResponse({'error': 'Chapter not found'}, status=404)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'registration/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')

@login_required
def profile_view(request):
    context = {
        'user': request.user
    }
    if request.user.is_student:
        context['student'] = request.user.student
    elif request.user.is_teacher:
        context['teacher'] = request.user.teacher
    
    return render(request, 'main/profile.html', context)