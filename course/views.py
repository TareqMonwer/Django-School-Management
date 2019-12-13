from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Section, Course, CourseAttendance
from .forms import SectionForm, CourseForm, CourseAttendanceForm

# Create your views here.

@login_required
def course(request):
    """
    Create course here
    """
    if request.method == 'POST':
        course_form = CourseForm(request.POST)
        if course_form.is_valid():
            course_form.save()
    form = CourseForm()
    context = {
        "form": form
    }
    return render(request, 'course/add_course.html', context)

def course_list(request):
    """
    Course list is here
    """
    if request.method == 'GET':
        all_course = Course.objects.all()
        context = {
            "all_course": all_course
        }
        return render(request, 'course/course_list.html', context)

@login_required
def section(request):
    """
    Create section here
    """
    if request.method == 'POST':
        section_form = SectionForm(request.POST)
        if section_form.is_valid():
            section_form.save()
    form = SectionForm()
    context = {
        "form": form
    }
    return render(request, 'course/add_section.html', context)

def section_list(request):
    """
    Section list is here
    """
    if request.method == 'GET':
        all_section = Section.objects.all()
        context = {
            "all_section": all_section
        }
        return render(request, 'course/section_list.html', context)

@login_required
def course_attendance(request):
    """
    Create course attendance here
    """
    if request.method == 'POST':
        course_attendance_form = CourseAttendanceForm(request.POST)
        if course_attendance_form.is_valid():
            course_attendance_form.save()
    form = CourseAttendanceForm()
    context = {
        "form": form
    }
    return render(request, 'course/add_course_attendance.html', context)

def course_attendance_list(request):
    """
    Course attendance list is here
    """
    if request.method == 'GET':
        all_course_attendance = CourseAttendance.objects.all()
        context = {
            "all_course_attendance": all_course_attendance
        }
        return render(request, 'course/course_attendance_list.html', context)
