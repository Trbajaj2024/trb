from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    roll_number = models.CharField(max_length=20, unique=True)
    grade = models.CharField(max_length=10)
    section = models.CharField(max_length=1)
    parent_name = models.CharField(max_length=100)
    parent_phone = models.CharField(max_length=15)

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    employee_id = models.CharField(max_length=20, unique=True)
    subject = models.CharField(max_length=50)
    qualification = models.CharField(max_length=100)

class Carousel(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    image = models.ImageField(upload_to='carousel/')
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

class Statistic(models.Model):
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=50)
    icon = models.CharField(max_length=50)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

class Program(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text="Font Awesome class name (e.g., fas fa-microscope)")
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    image = models.ImageField(upload_to='events/')
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-date']

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    image = models.ImageField(upload_to='testimonials/')
    text = models.TextField()
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

class Achievement(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    image = models.ImageField(upload_to='achievements/', blank=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date']

class Notice(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    for_students = models.BooleanField(default=True)
    for_teachers = models.BooleanField(default=True)

    class Meta:
        ordering = ['-date']

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"

class LiveClass(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    platform = models.CharField(max_length=50, choices=[('YouTube', 'YouTube'), ('Google Meet', 'Google Meet')])
    link = models.URLField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.title

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='courses/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_cached_subjects(self):
        cache_key = f'course_subjects_{self.id}'
        subjects = cache.get(cache_key)
        
        if subjects is None:
            subjects = list(self.subjects.all())
            cache.set(cache_key, subjects, timeout=3600)  # Cache for 1 hour
        
        return subjects

    def clear_cache(self):
        cache.delete(f'course_subjects_{self.id}')
        cache.delete(f'course_{self.id}')

class Subject(models.Model):
    course = models.ForeignKey(Course, related_name='subjects', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"

    def get_cached_chapters(self):
        cache_key = f'subject_chapters_{self.id}'
        chapters = cache.get(cache_key)
        
        if chapters is None:
            chapters = list(self.chapters.all())
            cache.set(cache_key, chapters, timeout=3600)
        
        return chapters

    def clear_cache(self):
        cache.delete(f'subject_chapters_{self.id}')
        self.course.clear_cache()

class Chapter(models.Model):
    subject = models.ForeignKey(Subject, related_name='chapters', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.subject.title} - {self.title}"

    def get_cached_lectures(self):
        cache_key = f'chapter_lectures_{self.id}'
        lectures = cache.get(cache_key)
        
        if lectures is None:
            lectures = list(self.video_lectures.all())
            cache.set(cache_key, lectures, timeout=3600)
        
        return lectures

    def clear_cache(self):
        cache.delete(f'chapter_lectures_{self.id}')
        self.subject.clear_cache()

class VideoLecture(models.Model):
    chapter = models.ForeignKey(Chapter, related_name='video_lectures', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    video_id = models.CharField(max_length=100)  # YouTube video ID
    order = models.IntegerField(default=0)
    duration = models.CharField(max_length=50, blank=True)  # Duration in format "HH:MM:SS"

    class Meta:
        ordering = ['order']

    @property
    def video_url(self):
        return f"https://www.youtube.com/embed/{self.video_id}"

    def __str__(self):
        return self.title

    def clear_cache(self):
        self.chapter.clear_cache()

# Signal handlers for cache invalidation
@receiver([post_save, post_delete], sender=Course)
def invalidate_course_cache(sender, instance, **kwargs):
    instance.clear_cache()

@receiver([post_save, post_delete], sender=Subject)
def invalidate_subject_cache(sender, instance, **kwargs):
    instance.clear_cache()

@receiver([post_save, post_delete], sender=Chapter)
def invalidate_chapter_cache(sender, instance, **kwargs):
    instance.clear_cache()

@receiver([post_save, post_delete], sender=VideoLecture)
def invalidate_lecture_cache(sender, instance, **kwargs):
    instance.clear_cache()

class AboutPage(models.Model):
    hero_title = models.CharField(max_length=200, default="About TRBSS")
    hero_subtitle = models.CharField(max_length=200, default="Nurturing Minds, Building Futures Since 1995")
    hero_image = models.ImageField(upload_to='about/', help_text="Hero background image")
    
    welcome_title = models.CharField(max_length=200, default="Welcome to Excellence")
    welcome_description = models.TextField()
    welcome_image = models.ImageField(upload_to='about/')
    
    class Meta:
        verbose_name_plural = "About Page"

class Feature(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text="Font Awesome class (e.g., fas fa-graduation-cap)")
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

class TimelineEvent(models.Model):
    year = models.CharField(max_length=4)
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

class CoreValue(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

class CallToAction(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.TextField()
    button_text = models.CharField(max_length=50)
    button_link = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    location = models.CharField(max_length=50, help_text="Where this CTA appears (e.g., about_page, home_page)")

    class Meta:
        ordering = ['location']

class AcademicLevel(models.Model):
    name = models.CharField(max_length=100)  # e.g., Primary, Secondary, Higher Secondary
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text="Font Awesome class name")
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='departments/')
    head_name = models.CharField(max_length=100)
    head_qualification = models.CharField(max_length=100)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

class Curriculum(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    academic_level = models.ForeignKey(AcademicLevel, on_delete=models.CASCADE)
    subjects = models.TextField(help_text="List of subjects, one per line")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.academic_level.name} - {self.title}"