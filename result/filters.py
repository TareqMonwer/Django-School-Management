import django_filters

from students.models import Student
from .models import Result, SubjectGroup

class ResultFilter(django_filters.FilterSet):
    student__temporary_id = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Temporary ID'
    )
    class Meta:
        model = Result
        fields = [
            'semester',
            'subject',
            'student__temporary_id'
        ]


class SubjectGroupFilter(django_filters.FilterSet):
    class Meta:
        model = SubjectGroup
        fields = [
            'department',
            'semester',
        ]
