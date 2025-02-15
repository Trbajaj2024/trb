from django.shortcuts import render
from .models import SchoolInfo, Faculty, Testimonial, Event, Announcement, Facility, Student, SchoolPolicy, VolunteerOpportunity, VolunteerRegistration, Payment, SocialMedia, LegalPage
from django.utils import timezone
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404
from .forms import ContactForm, NewsletterForm, ParentMessageForm, VolunteerRegistrationForm, PaymentForm
from django.contrib.auth.decorators import login_required
import time
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.cache import cache_page
from django.core.cache import cache

@cache_page(60 * 15)  # Cache for 15 minutes
def home(request):
    school_info = SchoolInfo.objects.first()
    # Get or set cached announcements
    announcements = cache.get('home_announcements')
    if announcements is None:
        announcements = Announcement.objects.filter(
            is_active=True
        ).order_by('-date_posted')[:5]
        cache.set('home_announcements', announcements, 60 * 15)
    latest_news = Announcement.objects.filter(
        is_active=True
    ).order_by('-date_posted')[5:9]  # Skip carousel items
    
    context = {
        'school_info': school_info,
        'announcements': announcements,
        'latest_news': latest_news,
    }
    return render(request, 'core/home.html', context)

def about(request):
    school_info = SchoolInfo.objects.first()
    faculty = Faculty.objects.all().order_by('role')
    facilities = Facility.objects.all().order_by('category')
    testimonials = Testimonial.objects.order_by('-date_added')[:6]
    
    # Group faculty by role
    faculty_by_role = {}
    for member in faculty:
        if member.role not in faculty_by_role:
            faculty_by_role[member.role] = []
        faculty_by_role[member.role].append(member)
    
    # Group facilities by category
    facilities_by_category = {}
    for facility in facilities:
        if facility.category not in facilities_by_category:
            facilities_by_category[facility.category] = []
        facilities_by_category[facility.category].append(facility)
    
    context = {
        'school_info': school_info,
        'faculty_by_role': faculty_by_role,
        'facilities_by_category': facilities_by_category,
        'testimonials': testimonials,
    }
    return render(request, 'core/about.html', context)

def academics(request):
    courses = Course.objects.all().order_by('code')
    context = {
        'courses': courses,
    }
    return render(request, 'core/academics.html', context)

def events(request):
    upcoming_events = Event.objects.filter(
        date__gte=timezone.now()
    ).order_by('date')
    past_events = Event.objects.filter(
        date__lt=timezone.now()
    ).order_by('-date')[:5]
    
    context = {
        'upcoming_events': upcoming_events,
        'past_events': past_events,
    }
    return render(request, 'core/events.html', context)

def contact(request):
    school_info = SchoolInfo.objects.first()
    success = False
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            message = form.save()
            
            # Send email notification
            subject = f"New Contact Form Submission: {message.subject}"
            email_body = f"""
            New message from {message.name}
            
            Email: {message.email}
            Phone: {message.phone}
            Type: {message.get_inquiry_type_display()}
            
            Message:
            {message.message}
            """
            
            try:
                send_mail(
                    subject,
                    email_body,
                    settings.DEFAULT_FROM_EMAIL,
                    [school_info.email],
                    fail_silently=False,
                )
            except Exception as e:
                # Log the error but don't show to user
                print(f"Email sending failed: {e}")
            
            messages.success(request, 'Your message has been sent successfully! We will get back to you soon.')
            return redirect('contact')
    else:
        form = ContactForm()
    
    context = {
        'school_info': school_info,
        'form': form,
    }
    return render(request, 'core/contact.html', context)

def parents(request):
    announcements = Announcement.objects.filter(
        is_active=True
    ).order_by('-date_posted')[:5]
    
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully subscribed to the newsletter!')
            return redirect('parents')
    else:
        form = NewsletterForm()
    
    context = {
        'announcements': announcements,
        'form': form,
    }
    return render(request, 'core/parents.html', context)

@login_required
def parents_dashboard(request):
    children = Student.objects.filter(parent_email=request.user.email)
    upcoming_events = Event.objects.filter(
        date__gte=timezone.now()
    ).order_by('date')[:5]
    volunteer_opportunities = VolunteerOpportunity.objects.filter(
        is_active=True,
        date__gte=timezone.now()
    ).order_by('date')[:5]
    recent_policies = SchoolPolicy.objects.filter(
        is_active=True
    ).order_by('-last_updated')[:5]

    context = {
        'children': children,
        'upcoming_events': upcoming_events,
        'volunteer_opportunities': volunteer_opportunities,
        'recent_policies': recent_policies,
    }
    return render(request, 'core/parents_dashboard.html', context)

@login_required
def school_policies(request):
    policies = SchoolPolicy.objects.filter(is_active=True).order_by('category', 'title')
    policies_by_category = {}
    
    for policy in policies:
        category = policy.get_category_display()
        if category not in policies_by_category:
            policies_by_category[category] = []
        policies_by_category[category].append(policy)

    context = {
        'policies_by_category': policies_by_category,
    }
    return render(request, 'core/school_policies.html', context)

@login_required
def volunteer_opportunities(request):
    opportunities = VolunteerOpportunity.objects.filter(
        is_active=True,
        date__gte=timezone.now()
    ).order_by('date')

    user_registrations = {
        reg.opportunity_id: reg
        for reg in VolunteerRegistration.objects.filter(parent=request.user)
    }

    context = {
        'opportunities': opportunities,
        'user_registrations': user_registrations,
    }
    return render(request, 'core/volunteer_opportunities.html', context)

@login_required
def register_volunteer(request, opportunity_id):
    opportunity = get_object_or_404(VolunteerOpportunity, id=opportunity_id)
    
    if request.method == 'POST':
        form = VolunteerRegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.opportunity = opportunity
            registration.parent = request.user
            registration.save()
            messages.success(request, 'Successfully registered for volunteer opportunity!')
            return redirect('volunteer_opportunities')
    else:
        form = VolunteerRegistrationForm()

    context = {
        'opportunity': opportunity,
        'form': form,
    }
    return render(request, 'core/register_volunteer.html', context)

@login_required
def contact_teacher(request, teacher_id):
    teacher = get_object_or_404(User, id=teacher_id)
    
    if request.method == 'POST':
        form = ParentMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = teacher
            message.save()
            messages.success(request, 'Message sent successfully!')
            return redirect('parents_dashboard')
    else:
        form = ParentMessageForm()

    context = {
        'teacher': teacher,
        'form': form,
    }
    return render(request, 'core/contact_teacher.html', context)

@login_required
def payment_portal(request):
    recent_payments = Payment.objects.filter(
        user=request.user
    ).order_by('-payment_date')[:5]
    
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.user = request.user
            payment.transaction_id = f"TXN{int(time.time())}"
            payment.status = 'pending'
            payment.save()
            
            # Here you would integrate with a payment gateway
            # For demonstration, we'll just mark it as completed
            payment.status = 'completed'
            payment.save()
            
            messages.success(request, 'Payment processed successfully!')
            return redirect('payment_portal')
    else:
        form = PaymentForm()

    context = {
        'form': form,
        'recent_payments': recent_payments,
    }
    return render(request, 'core/payment_portal.html', context)

def legal_page(request, slug):
    page = get_object_or_404(LegalPage, slug=slug, is_active=True)
    context = {
        'page': page,
    }
    return render(request, 'core/legal_page.html', context)

def get_footer_context():
    """Helper function to get common footer context"""
    return {
        'social_media': SocialMedia.objects.filter(is_active=True),
        'legal_pages': LegalPage.objects.filter(is_active=True),
        'school_info': SchoolInfo.objects.first(),
    }

def handler404(request, exception):
    return render(request, 'errors/404.html', status=404)

def handler500(request):
    return render(request, 'errors/500.html', status=500) 