from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    head = models.ForeignKey('core.Faculty', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

class Program(models.Model):
    PROGRAM_TYPES = [
        ('regular', 'Regular'),
        ('ap', 'Advanced Placement'),
        ('stem', 'STEM'),
        ('arts', 'Arts'),
        ('special', 'Special Program'),
    ]

    name = models.CharField(max_length=200)
    program_type = models.CharField(max_length=20, choices=PROGRAM_TYPES)
    description = models.TextField()
    requirements = models.TextField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='programs/', blank=True)

    def __str__(self):
        return f"{self.get_program_type_display()} - {self.name}"

class Course(models.Model):
    GRADE_LEVELS = [
        ('9', '9th Grade'),
        ('10', '10th Grade'),
        ('11', '11th Grade'),
        ('12', '12th Grade'),
        ('all', 'All Grades'),
    ]

    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    credits = models.DecimalField(max_digits=3, decimal_places=1)
    grade_level = models.CharField(max_length=3, choices=GRADE_LEVELS)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.SET_NULL, null=True, blank=True)
    prerequisites = models.ManyToManyField('self', blank=True, symmetrical=False)
    is_elective = models.BooleanField(default=False)
    syllabus = models.FileField(upload_to='syllabi/', blank=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

class AcademicCalendarEvent(models.Model):
    EVENT_TYPES = [
        ('exam', 'Examination'),
        ('holiday', 'Holiday'),
        ('ptm', 'Parent-Teacher Meeting'),
        ('activity', 'Academic Activity'),
    ]

    title = models.CharField(max_length=200)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    grade_levels = models.CharField(max_length=50, blank=True, 
        help_text="Leave blank for all grades or enter comma-separated grades (e.g., '9,10,11')")

    class Meta:
        ordering = ['start_date']

    def __str__(self):
        return f"{self.title} ({self.start_date})" 