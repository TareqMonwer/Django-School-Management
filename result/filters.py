import django_filters

from .models import Result

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
