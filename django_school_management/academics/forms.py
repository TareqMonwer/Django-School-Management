from collections.abc import Iterable
from typing import Type

from django.db.models import Model
from django.forms import ModelForm

from .models import Department, Semester, AcademicSession, Subject


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
