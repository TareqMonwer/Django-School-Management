import django_filters

from ..models import Student


class StudentFilterSet(django_filters.FilterSet):
    """FilterSet for Student API. Exposes department via batch__department."""
    department = django_filters.NumberFilter(field_name='batch__department')

    class Meta:
        model = Student
        fields = ['batch', 'is_alumni', 'is_dropped']
