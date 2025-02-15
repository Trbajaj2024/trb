from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import (
    Student, Course, Assignment, StudentAssignment,
    StudentAttendance, StudyResource
)

@login_required
def student_portal(request):
    try:
        student = request.user.student
    except Student.DoesNotExist:
        messages.error(request, "You don't have a student profile.")
        return redirect('home')

    # Get current courses
    current_courses = Course.objects.filter(
        enrollment__student=student,
        enrollment__status='active'
    )

    # Get upcoming assignments
    upcoming_assignments = StudentAssignment.objects.filter(
        student=student,
        assignment__due_date__gte=timezone.now(),
        status='pending'
    ).order_by('assignment__due_date')[:5]

    # Get recent grades
    recent_grades = StudentAssignment.objects.filter(
        student=student,
        status='graded'
    ).order_by('-assignment__due_date')[:5]

    # Get recent attendance
    recent_attendance = StudentAttendance.objects.filter(
        student=student
    ).order_by('-date')[:5]

    context = {
        'student': student,
        'current_courses': current_courses,
        'upcoming_assignments': upcoming_assignments,
        'recent_grades': recent_grades,
        'recent_attendance': recent_attendance,
    }
    return render(request, 'accounts/student_portal.html', context)

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    student = request.user.student
    
    # Verify enrollment
    if not course.enrollment_set.filter(student=student).exists():
        messages.error(request, "You are not enrolled in this course.")
        return redirect('student_portal')

    assignments = StudentAssignment.objects.filter(
        student=student,
        assignment__course=course
    ).order_by('-assignment__due_date')

    resources = StudyResource.objects.filter(
        course=course,
        is_active=True
    ).order_by('-created_at')

    context = {
        'course': course,
        'assignments': assignments,
        'resources': resources,
    }
    return render(request, 'accounts/course_detail.html', context)

@login_required
def submit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    student = request.user.student
    
    student_assignment, created = StudentAssignment.objects.get_or_create(
        student=student,
        assignment=assignment
    )

    if request.method == 'POST':
        form = AssignmentSubmissionForm(request.POST, request.FILES, instance=student_assignment)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.submitted_at = timezone.now()
            submission.status = 'late' if timezone.now() > assignment.due_date else 'submitted'
            submission.save()
            messages.success(request, 'Assignment submitted successfully!')
            return redirect('course_detail', course_id=assignment.course.id)
    else:
        form = AssignmentSubmissionForm(instance=student_assignment)

    context = {
        'assignment': assignment,
        'form': form,
        'student_assignment': student_assignment,
    }
    return render(request, 'accounts/submit_assignment.html', context)

@login_required
def attendance_record(request):
    student = request.user.student
    attendance = StudentAttendance.objects.filter(student=student)
    
    # Calculate attendance statistics
    total_days = attendance.count()
    present_days = attendance.filter(status='present').count()
    attendance_percentage = (present_days / total_days * 100) if total_days > 0 else 0

    context = {
        'attendance_records': attendance,
        'total_days': total_days,
        'present_days': present_days,
        'attendance_percentage': attendance_percentage,
    }
    return render(request, 'accounts/attendance_record.html', context)

@login_required
def study_resources(request):
    student = request.user.student
    courses = Course.objects.filter(enrollment__student=student)
    
    resources_by_course = {}
    for course in courses:
        resources = StudyResource.objects.filter(
            course=course,
            is_active=True
        ).order_by('-created_at')
        resources_by_course[course] = resources

    context = {
        'resources_by_course': resources_by_course,
    }
    return render(request, 'accounts/study_resources.html', context) 