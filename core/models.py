from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class SEOModel(models.Model):
    """Abstract base model for SEO fields"""
    meta_title = models.CharField(max_length=60, blank=True, help_text="Max 60 characters")
    meta_description = models.CharField(max_length=160, blank=True, help_text="Max 160 characters")
    meta_keywords = models.CharField(max_length=200, blank=True, help_text="Comma-separated keywords")
    
    class Meta:
        abstract = True

    def get_meta_title(self):
        return self.meta_title or self.title

    def get_meta_description(self):
        return self.meta_description or self.description[:160]

class SchoolInfo(models.Model):
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='school/')
    address = models.TextField()
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    mission_statement = models.TextField()
    vision = models.TextField()

    def __str__(self):
        return self.name

class Faculty(models.Model):
    name = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='faculty/')
    role = models.CharField(max_length=200)
    bio = models.TextField()
    email = models.EmailField()

    class Meta:
        verbose_name_plural = 'Faculty'

    def __str__(self):
        return self.name

class Testimonial(models.Model):
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=100)  # e.g., Student, Parent, Alumni
    photo = models.ImageField(upload_to='testimonials/', blank=True)
    content = models.TextField()
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.role}"

class Event(SEOModel):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='events/', blank=True)
    registration_required = models.BooleanField(default=False)
    max_participants = models.PositiveIntegerField(null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        indexes = [
            models.Index(fields=['date', 'is_active']),
            models.Index(fields=['slug']),
        ]

class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='announcements/', blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class NewsletterSubscription(models.Model):
    email = models.EmailField(unique=True)
    date_subscribed = models.DateTimeField(auto_now_add=True)
    is_parent = models.BooleanField(default=False)

    def __str__(self):
        return self.email

class Facility(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='facilities/')
    category = models.CharField(max_length=50, choices=[
        ('academic', 'Academic'),
        ('sports', 'Sports'),
        ('library', 'Library'),
        ('laboratory', 'Laboratory'),
        ('other', 'Other')
    ])
    features = models.TextField(help_text="Enter features separated by newlines")

    class Meta:
        verbose_name_plural = 'Facilities'

    def feature_list(self):
        return self.features.split('\n')

    def __str__(self):
        return self.name

class SchoolPolicy(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=50, choices=[
        ('academic', 'Academic'),
        ('behavioral', 'Behavioral'),
        ('attendance', 'Attendance'),
        ('safety', 'Safety'),
        ('general', 'General')
    ])
    last_updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'School Policies'

    def __str__(self):
        return self.title

class VolunteerOpportunity(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    slots_available = models.PositiveIntegerField()
    contact_person = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Volunteer Opportunities'

    def get_registered_count(self):
        return self.volunteerregistration_set.count()

    def __str__(self):
        return self.title

class VolunteerRegistration(models.Model):
    opportunity = models.ForeignKey(VolunteerOpportunity, on_delete=models.CASCADE)
    parent = models.ForeignKey(User, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('declined', 'Declined')
    ], default='pending')

    class Meta:
        unique_together = ['opportunity', 'parent']

    def __str__(self):
        return f"{self.parent.get_full_name()} - {self.opportunity.title}"

class ParentMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=200)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    replied_to = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.sender} to {self.recipient} - {self.subject}"

class Payment(models.Model):
    PAYMENT_TYPES = [
        ('fees', 'School Fees'),
        ('event', 'Event Payment'),
        ('donation', 'Donation'),
        ('other', 'Other')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=200)
    transaction_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded')
    ])
    payment_date = models.DateTimeField(auto_now_add=True)
    related_event = models.ForeignKey('Event', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_payment_type_display()} - {self.amount}"

class ContactMessage(models.Model):
    INQUIRY_TYPES = [
        ('general', 'General Inquiry'),
        ('admission', 'Admission Inquiry'),
        ('academic', 'Academic Question'),
        ('technical', 'Technical Support'),
        ('other', 'Other')
    ]

    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    inquiry_type = models.CharField(max_length=20, choices=INQUIRY_TYPES)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"

class SocialMedia(models.Model):
    platform = models.CharField(max_length=50, choices=[
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter'),
        ('instagram', 'Instagram'),
        ('linkedin', 'LinkedIn'),
        ('youtube', 'YouTube')
    ])
    url = models.URLField()
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Social Media Links'
        ordering = ['platform']

    def __str__(self):
        return self.get_platform_display()

class LegalPage(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    last_updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title 