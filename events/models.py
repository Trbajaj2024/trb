from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Event(models.Model):
    EVENT_TYPES = [
        ('academic', 'Academic'),
        ('sports', 'Sports'),
        ('cultural', 'Cultural'),
        ('ptm', 'Parent-Teacher Meeting'),
        ('other', 'Other')
    ]

    title = models.CharField(max_length=200)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    description = models.TextField()
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='events/', blank=True)
    registration_required = models.BooleanField(default=False)
    max_participants = models.PositiveIntegerField(null=True, blank=True)
    registration_deadline = models.DateTimeField(null=True, blank=True)
    organizer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_registered_count(self):
        return self.eventregistration_set.count()

    def is_registration_open(self):
        if not self.registration_required:
            return False
        if self.registration_deadline and self.registration_deadline < timezone.now():
            return False
        if self.max_participants and self.get_registered_count() >= self.max_participants:
            return False
        return True

    def __str__(self):
        return self.title

class EventRegistration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)
    num_guests = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled')
    ], default='pending')

    class Meta:
        unique_together = ['event', 'user']

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.event.title}" 