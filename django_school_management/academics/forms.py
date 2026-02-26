from collections.abc import Iterable
from typing import Type

from django.db.models import Model
from django.forms import ModelForm

from django import forms
from django.core.exceptions import ValidationError

from .models import Department, Semester, AcademicSession, Subject, Batch
from ..mixins.institute import get_user_institute


def create_model_form_factory(
        model_class: Type[Model],
        *,
        include_fields: Iterable[str] = None,
        exclude_fields: Iterable[str] = None
) -> Type[ModelForm]:
    class CreatedByExcludedForm(ModelForm):
        class Meta:
            model = model_class
            fields = include_fields if include_fields else '__all__'
            exclude = exclude_fields if exclude_fields else []

    return CreatedByExcludedForm


DepartmentForm = create_model_form_factory(Department, exclude_fields=['created_by', 'institute'])

SemesterForm = create_model_form_factory(Semester, exclude_fields=['created_by',])

AcademicSessionForm = create_model_form_factory(AcademicSession, exclude_fields=['created_by',])

SubjectForm = create_model_form_factory(Subject, exclude_fields=['created_by',])

BatchForm = create_model_form_factory(Batch, include_fields=['department', 'year', 'number'])


class BatchFormWithLabel(BatchForm):
    """Batch form with department label set from user's institute (Group vs Department)."""

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        if request and 'department' in self.fields:
            institute = get_user_institute(getattr(request, 'user', None))
            self.fields['department'].label = institute.department_label if institute else 'Department'


class BulkSemesterForm(forms.Form):
    """Form to create multiple semesters at once. Accepts e.g. '1-6' or '1,2,3,4'."""

    numbers = forms.CharField(
        label='Semester numbers',
        help_text='Enter a range (e.g. 1-6) or comma-separated numbers (e.g. 1,2,3,4).',
        widget=forms.TextInput(attrs={'placeholder': '1-6 or 1,2,3,4'}),
    )

    def clean_numbers(self):
        value = self.cleaned_data.get('numbers', '').strip()
        if not value:
            raise ValidationError('Enter at least one semester number.')
        numbers = set()
        for part in value.split(','):
            part = part.strip()
            if '-' in part:
                try:
                    a, b = part.split('-', 1)
                    a, b = int(a.strip()), int(b.strip())
                    if a > b:
                        a, b = b, a
                    for n in range(a, b + 1):
                        if n >= 1:
                            numbers.add(n)
                except ValueError:
                    raise ValidationError(f'Invalid range: {part}. Use e.g. 1-6.')
            else:
                try:
                    n = int(part)
                    if n >= 1:
                        numbers.add(n)
                except ValueError:
                    raise ValidationError(f'Invalid number: {part}.')
        if not numbers:
            raise ValidationError('Enter at least one valid semester number (1 or more).')
        existing = set(Semester.objects.filter(number__in=numbers).values_list('number', flat=True))
        if existing:
            raise ValidationError(f'Semester(s) already exist: {sorted(existing)}. Create only new numbers.')
        return sorted(numbers)
