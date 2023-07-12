import django_filters

from students.models import Student


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
        super(AlumniFilter, self).__init__(*args, **kwargs)
        self.filters['admission_student__name'].label = 'Name'
        self.filters['admission_student__choosen_department'].label = 'Department'
        self.filters['ac_session'].label = 'Academic Session'
