import django_filters

from django_school_management.students.models import Student
from django_school_management.mixins.institute import get_user_institute
from .models import Result, SubjectGroup


class ResultFilter(django_filters.FilterSet):
    student__temporary_id = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Temporary ID'
    )
    class Meta:
        model = Result
        fields = [
            'student__admission_student__choosen_department',
            'semester',
            'subject',
            'student__temporary_id'
        ]

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super(ResultFilter, self).__init__(*args, **kwargs)
        institute = get_user_institute(getattr(request, 'user', None)) if request else None
        dept_label = institute.department_label if institute else 'Department'
        sem_label = institute.semester_label if institute else 'Semester'
        self.filters['student__admission_student__choosen_department'].label = dept_label
        self.filters['semester'].label = sem_label


class SubjectGroupFilter(django_filters.FilterSet):
    class Meta:
        model = SubjectGroup
        fields = [
            'department',
            'semester',
        ]

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super(SubjectGroupFilter, self).__init__(*args, **kwargs)
        institute = get_user_institute(getattr(request, 'user', None)) if request else None
        dept_label = institute.department_label if institute else 'Department'
        sem_label = institute.semester_label if institute else 'Semester'
        self.filters['department'].label = dept_label
        self.filters['semester'].label = sem_label
