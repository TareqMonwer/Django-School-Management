from django import forms
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
