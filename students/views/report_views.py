import datetime
from django.shortcuts import render

from students.models import AdmissionStudent
from academics.models import Department
from students.utils.bd_zila import ALL_ZILA


def counsel_monthly_report(request):
    # Find last month to generate last months report.
    date = datetime.date.today()
    first_day_of_month = date.replace(day=1)
    last_month = first_day_of_month - datetime.timedelta(days=1)

    total_applications = AdmissionStudent.objects.order_by('-created').filter(
        created__year=date.year,
        created__month=last_month.month)

    # Online/offline applications
    online_applications = total_applications.filter(application_type='1')   # 1 is online
    offline_applications = total_applications.filter(application_type='2')

    total_admission = AdmissionStudent.objects.filter(admitted=True).filter(
        created__year=date.year,
        created__month=last_month.month)

    # Online/offline admissions
    total_admission_online = total_admission.filter(application_type='1')   # 1 is online
    total_admission_offline = total_admission.filter(application_type='2')   # 2 is offline

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
        departmental_records[department.name] = {
            'applications_count': total_applications.filter(department_choice=department).count(),
            'admission_count': total_admission.filter(choosen_department=department).count(),
            # TODO: get migrated students
            'missed': total_applications.filter(department_choice=department, admitted=False).count()
        }

    zila_records = {}
    for k, v in ALL_ZILA:
        application_count = total_applications.filter(city=k).count()
        admission_count = total_admission.filter(city=k).count()
        if application_count > 0 or admission_count > 0:
            zila_records[v] = {
                'application_count': application_count,
                'admission_count': admission_count
            }

    ctx = {
        'date': date,
        'report_month': last_month.strftime('%B'),
        'total_applications': total_applications.count(),
        'total_admissions': total_admission.count(),
        'online_applications': online_applications.count(),
        'offline_applications': offline_applications.count(),
        'total_admission_online': total_admission_online.count(),
        'total_admission_offline': total_admission_offline.count(),
        'departmental_records': departmental_records,
        'zila_records': zila_records,
    }
    return render(request, 'students/reports/counsel_monthly_report.html', ctx)
