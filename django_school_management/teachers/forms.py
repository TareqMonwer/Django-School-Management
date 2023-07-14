from django import forms
from .models import Teacher, Designation


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['name', 'photo', 'date_of_birth',
                  'designation', 'expertise',
                  'mobile', 'email', ]
        widgets = {
            'date_of_birth': forms.TextInput({'type': 'date'}),
        }


class TeacherDesignationForm(forms.ModelForm):
    class Meta:
        model = Designation
        fields = '__all__'
