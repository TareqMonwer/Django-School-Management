from django.shortcuts import render

from students.models import AdmissionStudent
from academics.models import Department


def counsel_monthly_report(request):
    total_applications = AdmissionStudent.objects.order_by('-created')
    # TODO: get online/offline registrants
    # online_applications = total_applications.filter(application_method='online')
    # offline_applications = total_applications.filter(application_method='offline')

    total_admission = AdmissionStudent.objects.filter(admitted=True)
    # TODO: get online/offline admissions
    # total_admission_online = total_admission.filter(application_method='online')
    # total_admission_offline = total_admission.filter(application_method='offline')

    # TODO: Report By Department
    departments = Department.objects.all()
    # Illustration for how departmental tale will be stored and used in template.
    # {
    #     'cmt': {'applications': 100, 'admission': 30, 'migrated': 2, 'missed': 4},
    #     'aidt': {'applications': 100, 'admission': 30, 'migrated': 2, 'missed': 4},
    #     'tel': {'applications': 100, 'admission': 30, 'migrated': 2, 'missed': 4}
    # }
    departmental_records = {}
    for department in departments:
        # applications
        departmental_records[department.name] = {
            'applications_count': total_applications.filter(choosen_department=department).count(),
            'admission_count': total_admission.filter(choosen_department=department).count(),
            # TODO: get migrated students
            'missed': total_applications.filter(choosen_department=department, admitted=False).count()
        }

    # TODO: Implement records by Cities

    ctx = {
        'total_applications': total_applications.count(),
        'total_admissions': total_admission.count(),
        'departmental_records': departmental_records,
    }
    dc = departmental_records['Computer']
    print(dc, 'DC')
    return render(request, 'students/reports/counsel_monthly_report.html', ctx)
