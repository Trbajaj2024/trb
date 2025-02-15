from django.shortcuts import render, get_object_or_404
from .models import Department, Program, Course, AcademicCalendarEvent
from django.utils import timezone

def academics(request):
    departments = Department.objects.all()
    programs = Program.objects.all().order_by('program_type')
    upcoming_events = AcademicCalendarEvent.objects.filter(
        end_date__gte=timezone.now().date()
    ).order_by('start_date')[:5]
    
    # Group programs by type
    programs_by_type = {}
    for program in programs:
        program_type = program.get_program_type_display()
        if program_type not in programs_by_type:
            programs_by_type[program_type] = []
        programs_by_type[program_type].append(program)

    context = {
        'departments': departments,
        'programs_by_type': programs_by_type,
        'upcoming_events': upcoming_events,
    }
    return render(request, 'academics/academics.html', context)

def department_detail(request, pk):
    department = get_object_or_404(Department, pk=pk)
    courses = Course.objects.filter(department=department).order_by('grade_level', 'code')
    
    # Group courses by grade level
    courses_by_grade = {}
    for course in courses:
        grade = course.get_grade_level_display()
        if grade not in courses_by_grade:
            courses_by_grade[grade] = []
        courses_by_grade[grade].append(course)

    context = {
        'department': department,
        'courses_by_grade': courses_by_grade,
    }
    return render(request, 'academics/department_detail.html', context)

def program_detail(request, pk):
    program = get_object_or_404(Program, pk=pk)
    courses = Course.objects.filter(program=program).order_by('grade_level', 'code')

    context = {
        'program': program,
        'courses': courses,
    }
    return render(request, 'academics/program_detail.html', context)

def academic_calendar(request):
    events = AcademicCalendarEvent.objects.filter(
        end_date__gte=timezone.now().date()
    ).order_by('start_date')

    context = {
        'events': events,
    }
    return render(request, 'academics/calendar.html', context) 