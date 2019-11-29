from django.forms import ModelForm
from .models import Teacher, Designation


class TeacherForm(ModelForm):
    class Meta:
        model = Teacher
        fields = ['name', 'photo', 'date_of_birth',
                  'designation', 'expertise',
                  'mobile', 'email', ]


class TeacherDesignationForm(ModelForm):
    class Meta:
        model = Designation
        fields = '__all__'
