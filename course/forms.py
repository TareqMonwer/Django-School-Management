from django.forms import ModelForm

from .models import Section, Course, CourseAttendance


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
