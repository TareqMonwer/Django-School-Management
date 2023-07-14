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
            'fathers_name',
            'mothers_name',
            'date_of_birth',
            'city',
            'current_address',
            'permanent_address',
            'mobile_number',
            'guardian_mobile_number',
            'email',
            'tribal_status',
            'children_of_freedom_fighter',
            'department_choice',
            'exam_name',
            'passing_year',
            'group',
            'board',
            'ssc_roll',
            'ssc_registration',
            'gpa',
            'photo',
            'marksheet_image',
            'admission_policy_agreement',
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
            'current_address',
            'permanent_address',
            'mobile_number',
            'email',
            'choosen_department',
            'admitted',
            'paid',
            'rejected',
        ]
        widgets = {
            'date_of_birth': forms.TextInput({'type': 'date'}),
        }


class CounselingDataForm(forms.ModelForm):
    class Meta:
        model = CounselingComment
        fields = ['comment', ]


class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = (
            'roll',
            'registration_number',
            'semester',
            'guardian_mobile',
            'is_alumni', 'is_dropped'
        )
