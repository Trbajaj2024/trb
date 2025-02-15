from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, unique=True)
    grade = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    parent_email = models.EmailField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.student_id}"

class Course(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20)
    description = models.TextField()
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    students = models.ManyToManyField(Student, through='Enrollment')

    def __str__(self):
        return f"{self.code} - {self.name}"

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.CharField(max_length=2, blank=True, null=True)
    enrollment_date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ['student', 'course']

class StudentAttendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=[
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused')
    ])
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ['student', 'date']
        ordering = ['-date']

    def __str__(self):
        return f"{self.student} - {self.date} - {self.status}"

class Assignment(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateTimeField()
    points_possible = models.DecimalField(max_digits=5, decimal_places=2)
    attachment = models.FileField(upload_to='assignments/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course.code} - {self.title}"

class StudentAssignment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(null=True, blank=True)
    submission_file = models.FileField(upload_to='submissions/', blank=True)
    grade = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    feedback = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Not Submitted'),
        ('submitted', 'Submitted'),
        ('late', 'Submitted Late'),
        ('graded', 'Graded')
    ], default='pending')

    class Meta:
        unique_together = ['student', 'assignment']

    def __str__(self):
        return f"{self.student} - {self.assignment}"

class StudyResource(models.Model):
    RESOURCE_TYPES = [
        ('document', 'Document'),
        ('video', 'Video'),
        ('link', 'External Link'),
        ('book', 'Book Reference')
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    file = models.FileField(upload_to='resources/', blank=True)
    url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.course.code} - {self.title}" 