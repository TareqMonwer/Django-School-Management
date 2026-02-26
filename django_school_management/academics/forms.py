from collections.abc import Iterable
from typing import Type

from django.db.models import Model
from django.forms import ModelForm

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
