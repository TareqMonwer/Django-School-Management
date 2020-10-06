from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import Tab, TabHolder
from crispy_forms.layout import (Layout, Field,
                                ButtonHolder, Submit)
from .models import AdmissionStudent

class StudentForm(forms.ModelForm):
    class Meta:
        model = AdmissionStudent
        fields = [
            'name',
            'photo',
            'fathers_name',
            'mothers_name',
            'date_of_birth',
            'last_exam_roll',
            'current_address',
            'permanent_address',
            'last_exam_registration',
            'department_choice',
            'mobile_number',
            'email',
            'last_exam_name',
            'last_exam_result'
        ]
        widgets = {
            'date_of_birth': forms.TextInput({'type': 'date'}),
        }
