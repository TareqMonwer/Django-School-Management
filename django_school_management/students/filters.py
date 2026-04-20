import django_filters

from django_school_management.students.models import Student
from django_school_management.mixins.institute import get_user_institute


class AlumniFilter(django_filters.FilterSet):
    class Meta:
        model = Student
        fields = [
            'admission_student__name',
            'admission_student__choosen_department',
            'roll',
            'ac_session',
            'batch'
        ]

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super(AlumniFilter, self).__init__(*args, **kwargs)
        self.filters['admission_student__name'].label = 'Name'
        institute = get_user_institute(getattr(request, 'user', None)) if request else None
        dept_label = institute.department_label if institute else 'Department'
        self.filters['admission_student__choosen_department'].label = dept_label
        self.filters['ac_session'].label = 'Academic Session'
