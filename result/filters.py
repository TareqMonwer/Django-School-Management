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
            'student__admission_student__choosen_department',
            'semester',
            'subject',
            'student__temporary_id'
        ]

    def __init__(self, *args, **kwargs):
        super(ResultFilter, self).__init__(*args, **kwargs)
        self.filters['student__admission_student__choosen_department'].label = 'Department'


class SubjectGroupFilter(django_filters.FilterSet):
    class Meta:
        model = SubjectGroup
        fields = [
            'department',
            'semester',
        ]
