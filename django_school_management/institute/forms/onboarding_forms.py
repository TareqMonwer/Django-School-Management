from django import forms
from django.db import models
from django_countries.fields import CountryField

from django_school_management.institute.models import (
    InstituteProfile,
    INSTITUTE_TYPE_CHOICES,
)
from django_school_management.academics.models import Department, AcademicSession


FC = {'class': 'form-control'}


class OnboardingStep1Form(forms.ModelForm):
    """Institute profile basics including institute type."""

    class Meta:
        model = InstituteProfile
        fields = [
            'name', 'country', 'logo', 'motto', 'description',
            'date_of_estashment', 'institute_type',
        ]
        widgets = {
            'name': forms.TextInput(attrs={**FC, 'placeholder': 'Your institute name'}),
            'date_of_estashment': forms.DateInput(attrs={**FC, 'type': 'date'}),
            'motto': forms.Textarea(attrs={**FC, 'rows': 2, 'placeholder': 'Institute motto'}),
            'description': forms.Textarea(attrs={**FC, 'rows': 3, 'placeholder': 'Brief description'}),
            'institute_type': forms.Select(attrs={**FC}),
        }
        labels = {
            'date_of_estashment': 'Date of Establishment',
            'institute_type': 'Type of institution',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Show institute types in onboarding priority order: school, madrasah, polytechnic
        self.fields['institute_type'].choices = [('', '---------')] + list(INSTITUTE_TYPE_CHOICES)
        if 'country' in self.fields:
            self.fields['country'].widget.attrs.update(FC)


class OnboardingDepartmentForm(forms.Form):
    """Plain form for adding new departments during onboarding.
    All fields optional so empty rows are silently skipped."""

    name = forms.CharField(
        max_length=255, required=False,
        widget=forms.TextInput(attrs={**FC, 'placeholder': 'e.g. Computer Science'}),
    )
    short_name = forms.CharField(
        max_length=5, required=False,
        widget=forms.TextInput(attrs={**FC, 'placeholder': 'e.g. CSE'}),
    )
    code = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={**FC, 'placeholder': 'e.g. 101'}),
    )


OnboardingDepartmentFormSet = forms.formset_factory(
    OnboardingDepartmentForm,
    extra=1,
    max_num=20,
)


class OnboardingAcademicSessionForm(forms.ModelForm):
    """Academic session for onboarding."""

    class Meta:
        model = AcademicSession
        fields = ['year']
        widgets = {
            'year': forms.NumberInput(attrs={**FC, 'placeholder': 'e.g. 2026'}),
        }


class LoadSubjectsFromCurriculumForm(forms.Form):
    """Select curriculum and class range for loading subjects during onboarding."""

    curriculum = forms.ModelChoiceField(
        queryset=None,
        required=True,
        empty_label='Select curriculum',
        widget=forms.Select(attrs={**FC}),
        label='Curriculum',
    )
    class_range = forms.MultipleChoiceField(
        required=True,
        choices=[
            ('1-5', 'Class 1–5 (Ebtedayi / Primary)'),
            ('6-10', 'Class 6–10 (Dakhil / SSC)'),
            ('1-10', 'Class 1–10 (Full SSC)'),
            ('11-12', 'Class 11–12 (HSC)'),
        ],
        widget=forms.CheckboxSelectMultiple,
        label='Classes to load subjects for',
    )

    def __init__(self, *args, **kwargs):
        self.institute = kwargs.pop('institute', None)
        super().__init__(*args, **kwargs)
        if self.institute:
            from django_school_management.curriculum.models import Curriculum
            qs = Curriculum.objects.filter(is_active=True)
            itype = getattr(self.institute, 'institute_type', None)
            if itype:
                qs = qs.filter(models.Q(institute_type=itype) | models.Q(institute_type=''))
            self.fields['curriculum'].queryset = qs.order_by('display_order', 'name')
        else:
            from django_school_management.curriculum.models import Curriculum
            self.fields['curriculum'].queryset = Curriculum.objects.filter(is_active=True).order_by('display_order', 'name')

    def get_class_numbers(self):
        """Expand class_range choices to list of ints."""
        numbers = set()
        for r in self.cleaned_data.get('class_range', []):
            if r == '1-5':
                numbers.update(range(1, 6))
            elif r == '6-10':
                numbers.update(range(6, 11))
            elif r == '1-10':
                numbers.update(range(1, 11))
            elif r == '11-12':
                numbers.update(range(11, 13))
        return sorted(numbers)
