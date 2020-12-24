from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import Tab, TabHolder
from crispy_forms.layout import (
    Layout, Field, ButtonHolder, Submit
)
from .models import AdmissionStudent, CounselingComment, Student


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
            'city',
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


class AdmissionForm(forms.ModelForm):
    class Meta:
        model = AdmissionStudent
        fields = [
            'choosen_department',
        ]


class StudentRegistrantUpdateForm(forms.ModelForm):
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
            'mobile_number',
            'email',
            'last_exam_name',
            'last_exam_result',
            'choosen_department',
            'admitted',
            'rejected',
        ]
        widgets = {
            'date_of_birth': forms.TextInput({'type': 'date'}),
        }


class CounselingDataForm(forms.ModelForm):
    class Meta:
        model = CounselingComment
        fields = ['comment', 'counselor']


class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'roll', 'registration_number',
            'semester', 'guardian_mobile',
            'is_alumni', 'is_dropped'
        ]
