import re
from datetime import date

from django import forms
from django.core.validators import FileExtensionValidator
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import Tab, TabHolder
from crispy_forms.layout import (
    Layout, Field, ButtonHolder, Submit
)

from django_school_management.institute.models import EducationBoard
from django_school_management.institute.education_boards import (
    COUNTRY_BD,
    BD_GROUPS,
    APPLYING_FOR_CLASS_MIN,
    APPLYING_FOR_CLASS_MAX,
    APPLYING_FOR_CLASS_JSC_START,
)
from .models import AdmissionStudent, CounselingComment, Student

MAX_UPLOAD_SIZE_MB = 5


def _is_bd(institute):
    """True if institute has country set to Bangladesh."""
    if not institute or not getattr(institute, 'country', None):
        return False
    code = getattr(institute.country, 'code', institute.country) or str(institute.country)
    return code == COUNTRY_BD


class StudentForm(forms.ModelForm):
    """Admission form. When institute is school/madrasah, academic fields are optional."""

    class Meta:
        model = AdmissionStudent
        fields = [
            'name',
            'fathers_name',
            'mothers_name',
            'date_of_birth',
            'gender',
            'city',
            'current_address',
            'permanent_address',
            'mobile_number',
            'guardian_mobile_number',
            'email',
            'tribal_status',
            'department_choice',
            'applying_for_class',
            'board',
            'ssc_roll',
            'ssc_registration',
            'gpa',
            'exam_name',
            'passing_year',
            'group',
            'photo',
            'marksheet_image',
            'admission_policy_agreement',
            'admit_to_semester',
        ]
        widgets = {
            'date_of_birth': forms.TextInput({'type': 'date'}),
            'gpa': forms.NumberInput(attrs={'min': '0', 'max': '5', 'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        self.institute = kwargs.pop('institute', None)
        super().__init__(*args, **kwargs)
        # Gender: required for all
        if 'gender' in self.fields:
            self.fields['gender'].required = True
        # BD-only fields: show applying_for_class only for school/madrasah, admit_to_semester only for polytechnic
        if not _is_bd(self.institute):
            self.fields.pop('applying_for_class', None)
            self.fields.pop('admit_to_semester', None)
        else:
            if self.institute and self.institute.is_school_or_madrasah:
                self.fields.pop('admit_to_semester', None)
                self.fields['applying_for_class'].required = False
                self.fields['applying_for_class'].widget = forms.Select(
                    choices=[('', '---------')] + [(i, 'Class %s' % i) for i in range(APPLYING_FOR_CLASS_MIN, APPLYING_FOR_CLASS_MAX + 1)]
                )
            elif self.institute and self.institute.is_polytechnic:
                self.fields.pop('applying_for_class', None)
                self.fields['admit_to_semester'].required = False
                self.fields['admit_to_semester'].widget = forms.Select(
                    choices=[('', '---------'), (1, '1st Semester'), (4, '4th Semester (direct)')]
                )
            else:
                self.fields.pop('applying_for_class', None)
                self.fields.pop('admit_to_semester', None)
        if self.institute:
            self.fields['department_choice'].queryset = (
                self.fields['department_choice'].queryset.filter(institute=self.institute)
            )
            self.fields['department_choice'].label = (
                self.institute.department_label or 'Department'
            )
            if self.institute.is_school_or_madrasah:
                for f in ('exam_name', 'passing_year', 'group', 'board',
                          'ssc_roll', 'ssc_registration', 'gpa', 'marksheet_image'):
                    if f in self.fields:
                        self.fields[f].required = False
                if _is_bd(self.institute):
                    boards_qs = EducationBoard.get_boards_for_country(self.institute.country)
                    self.fields['board'].widget = forms.Select(
                        choices=[('', '---------')] + [(b.name, b.name) for b in boards_qs]
                    )
                    self.fields['board'].label = 'Board (from where result is obtained)'
                    self.fields['ssc_roll'].label = 'JSC/JDC Roll No.'
                    self.fields['ssc_registration'].label = 'JSC/JDC Registration No.'
                    self.fields['gpa'].label = 'Obtained Result (GPA out of 5.00)'
                    # BD school/madrasah: only applying_for_class + JSC section (no exam_name, passing_year, group)
                    for f in ('exam_name', 'passing_year', 'group'):
                        self.fields.pop(f, None)
            elif self.institute.is_polytechnic and _is_bd(self.institute):
                boards_qs = EducationBoard.get_boards_for_country(self.institute.country)
                self.fields['board'].widget = forms.Select(
                    choices=[('', '---------')] + [(b.name, b.name) for b in boards_qs]
                )
                self.fields['group'].widget = forms.Select(
                    choices=[('', '---------')] + list(BD_GROUPS)
                )

    def clean_gpa(self):
        gpa = self.cleaned_data.get('gpa')
        if gpa is not None and (gpa < 0 or gpa > 5):
            raise forms.ValidationError("GPA must be between 0.00 and 5.00.")
        return gpa

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

    def _check_file_size(self, field_name):
        f = self.cleaned_data.get(field_name)
        if f and hasattr(f, 'size') and f.size > MAX_UPLOAD_SIZE_MB * 1024 * 1024:
            raise forms.ValidationError(f"File must be under {MAX_UPLOAD_SIZE_MB} MB.")
        return f

    def clean_photo(self):
        return self._check_file_size('photo')

    def clean_marksheet_image(self):
        return self._check_file_size('marksheet_image')

    def clean(self):
        data = super().clean()
        if not data:
            return data
        # BD school/madrasah: require JSC/JDC fields when applying for class 9 or 10
        if _is_bd(self.institute) and self.institute and self.institute.is_school_or_madrasah:
            applying = data.get('applying_for_class')
            if applying is not None:
                try:
                    applying = int(applying)
                except (TypeError, ValueError):
                    applying = None
            if applying is not None and applying >= APPLYING_FOR_CLASS_JSC_START:
                for f in ('ssc_roll', 'ssc_registration', 'gpa', 'board'):
                    if f in self.fields and not data.get(f):
                        self.add_error(f, forms.ValidationError('This field is required for Class 9/10 admission.'))
        # BD polytechnic: admit_to_semester 4 only valid when HSC Science
        if _is_bd(self.institute) and self.institute and self.institute.is_polytechnic:
            admit_sem = data.get('admit_to_semester')
            if admit_sem is not None:
                try:
                    admit_sem = int(admit_sem)
                except (TypeError, ValueError):
                    admit_sem = None
            if admit_sem == 4:
                if data.get('exam_name') != 'HSC' or data.get('group') != 'Science':
                    self.add_error('admit_to_semester', forms.ValidationError(
                        'Direct admission to 4th semester is only for HSC Science passers.'
                    ))
        return data

    def clean_admit_to_semester(self):
        val = self.cleaned_data.get('admit_to_semester')
        if val is not None and val != '':
            try:
                return int(val)
            except (TypeError, ValueError):
                pass
        return None

    def clean_applying_for_class(self):
        val = self.cleaned_data.get('applying_for_class')
        if val is not None and val != '':
            try:
                n = int(val)
                if APPLYING_FOR_CLASS_MIN <= n <= APPLYING_FOR_CLASS_MAX:
                    return n
            except (TypeError, ValueError):
                pass
        return None


class AdmissionForm(forms.ModelForm):
    """Admit form: set choosen_department (polytechnic counselling)."""

    class Meta:
        model = AdmissionStudent
        fields = [
            'choosen_department',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.department_choice_id:
            institute = getattr(self.instance.department_choice, 'institute', None)
            if institute:
                self.fields['choosen_department'].queryset = (
                    self.fields['choosen_department'].queryset.filter(institute=institute)
                )


class StudentRegistrantUpdateForm(forms.ModelForm):
    class Meta:
        model = AdmissionStudent
        fields = [
            'name',
            'photo',
            'fathers_name',
            'mothers_name',
            'date_of_birth',
            'gender',
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

    def __init__(self, *args, **kwargs):
        show_choosen_department = kwargs.pop('show_choosen_department', True)
        super().__init__(*args, **kwargs)
        if not show_choosen_department and 'choosen_department' in self.fields:
            self.fields.pop('choosen_department')


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
