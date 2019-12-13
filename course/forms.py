from django.forms import ModelForm

from .models import (
    Section,
    Course,
    CourseAttendance,
    CourseAssignToTeacher,
    CourseAssignToStudent
)


class SectionForm(ModelForm):
    class Meta:
        model = Section
        fields = '__all__'


class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = '__all__'


class CourseAttendanceForm(ModelForm):
    class Meta:
        model = CourseAttendance
        fields = '__all__'


class CourseAssignToTeacherForm(ModelForm):
    class Meta:
        model = CourseAssignToTeacher
        fields = '__all__'


class CourseAssignToStudentForm(ModelForm):
    class Meta:
        model = CourseAssignToStudent
        fields = '__all__'
