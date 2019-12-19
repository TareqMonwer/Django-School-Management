from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from students.models import Student, Semester, Department

from .models import (
    Section,
    Course,
    CourseAttendance,
    CourseAssignToTeacher,
    CourseAssignToStudent,
    DailyAttendance
)
from .forms import (
    SectionForm,
    CourseForm,
    CourseAttendanceForm,
    CourseAssignToTeacherForm,
    CourseAssignToStudentForm,
)

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

@login_required
def course_assign_to_teacher(request):
    """
    Course assign to teacher form here
    """
    if request.method == 'POST':
        course_assign_to_teacher_form = CourseAssignToTeacherForm(request.POST)
        if course_assign_to_teacher_form.is_valid():
            course_assign_to_teacher_form.save()
    form = CourseAssignToTeacherForm()
    context = {
        "form": form
    }
    return render(request, 'course/add_course_assign_to_teacher.html', context)

def course_assign_to_teacher_list(request):
    """
    Course assign to teacher list is here
    """
    if request.method == 'GET':
        all_course_assign_to_teacher = CourseAssignToTeacher.objects.all()
        context = {
            "all_course_assign_to_teacher": all_course_assign_to_teacher
        }
        return render(request, 'course/course_assign_to_teacher_list.html', context)

@login_required
def course_assign_to_student(request):
    """
    Course assign to student form here
    """
    if request.method == 'POST':
        course_assign_to_student_form = CourseAssignToStudentForm(request.POST)
        if course_assign_to_student_form.is_valid():
            course_assign_to_student_form.save()
    form = CourseAssignToStudentForm()
    context = {
        "form": form
    }
    return render(request, 'course/add_course_assign_to_student.html', context)

def course_assign_to_student_list(request):
    """
    Course assign to student list is here
    """
    if request.method == 'GET':
        all_course_assign_to_student = CourseAssignToStudent.objects.all()
        context = {
            "all_course_assign_to_student": all_course_assign_to_student
        }
        return render(request, 'course/course_assign_to_student_list.html', context)


def daily_attendance(request):
    formset = modelformset_factory(DailyAttendance, fields=('__all__'))
    sem = Semester.objects.get(id=1)
    dept = Department.objects.get(id=1)
    if request.method == 'POST':
        form = formset(request.POST)
        isinstances = form.save()
        return render(request, 'course/attendance_daily.html', {'form': form})
    form = formset(queryset=Student.objects.filter(
        semester=sem, department=dept)[:10])
    return render(request, 'course/attendance_daily.html', {'form': form})
