import re
from datetime import date

from django import forms
from django.core.validators import FileExtensionValidator
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import Tab, TabHolder
from crispy_forms.layout import (
    Layout, Field, ButtonHolder, Submit
)
from .models import AdmissionStudent, CounselingComment, Student

MAX_UPLOAD_SIZE_MB = 5


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
            'gpa': forms.NumberInput(attrs={'min': '0', 'max': '5', 'step': '0.01'}),
        }

    def clean_mobile_number(self):
        value = self.cleaned_data.get('mobile_number', '')
        if value and not re.match(r'^\d{11}$', value):
            raise forms.ValidationError("Enter an 11-digit mobile number.")
        return value

    def clean_guardian_mobile_number(self):
        value = self.cleaned_data.get('guardian_mobile_number', '')
        if value and not re.match(r'^\d{11}$', value):
            raise forms.ValidationError("Enter an 11-digit mobile number.")
        return value

    def clean_date_of_birth(self):
        dob = self.cleaned_data.get('date_of_birth')
        if dob and dob >= date.today():
            raise forms.ValidationError("Date of birth must be in the past.")
        return dob

    def clean_gpa(self):
        gpa = self.cleaned_data.get('gpa')
        if gpa is not None and (gpa < 0 or gpa > 5):
            raise forms.ValidationError("GPA must be between 0.00 and 5.00.")
        return gpa

    def _check_file_size(self, field_name):
        f = self.cleaned_data.get(field_name)
        if f and hasattr(f, 'size') and f.size > MAX_UPLOAD_SIZE_MB * 1024 * 1024:
            raise forms.ValidationError(f"File must be under {MAX_UPLOAD_SIZE_MB} MB.")
        return f

    def clean_photo(self):
        return self._check_file_size('photo')

    def clean_marksheet_image(self):
        return self._check_file_size('marksheet_image')


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
