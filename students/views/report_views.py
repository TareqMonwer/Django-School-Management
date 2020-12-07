import datetime
from django.shortcuts import render
from django.http import JsonResponse

from students.models import AdmissionStudent
from academics.models import Department
from students.utils.bd_zila import ALL_ZILA


def get_departments_record(departments_qs, applications, admissions):
    """
    Takes all departments, all applications (non-admitted students),
    admitted students as admissions and  returns a dictionary containing
    all required information as shown here:
    {
        'department1': {'applications': 100, 'admission': 30, 'migrated_to': 2, 'migrated_from: 3, 'missed': 4},
        'department2': {'applications': 100, 'admission': 30, 'migrated_to': 2, 'migrated_from: 3, 'missed': 4},
    }
    """
    departmental_records = {}
    for department in departments_qs:
        departmental_records[department.name] = {
            'applications_count': applications.filter(department_choice=department).count(),
            'admission_count': admissions.filter(choosen_department=department).count(),
            'migrated_from_count': admissions.filter(department_choice=department,
                                                     migration_status__icontains='from').count(),
            'migrated_to_count': admissions.filter(choosen_department=department,
                                                   migration_status__icontains='from').count(),
            'missed': applications.filter(department_choice=department, rejected=True).count(),
            'creation_status': applications[0].created
        }
    return departmental_records


def get_active_cities_record(cities, applications, admissions):
    """
    Takes list of all zila ('1', 'Zila Name), all applications (non-admitted students),
    admitted students as admissions and  returns a dictionary containing total
    number of applications and admissions.
    """
    zila_records = {}
    for k, v in cities:
        application_count = applications.filter(city=k).count()
        admission_count = admissions.filter(city=k).count()
        if application_count > 0 or admission_count > 0:
            zila_records[v] = {
                'application_count': application_count,
                'admission_count': admission_count
            }
    return zila_records


def counsel_monthly_report(request, response_type='html', date_param=None):
    """
    Renders a template containing last mont's report of counsel (admission, application related stuff).
    """
    # Find last month(if month is not given in date_param) 
    # to generate last months report.
    if date_param:
        date = date_param.date()
        report_month = date.month
    else:
        date = datetime.date.today()
        first_day_of_month = date.replace(day=1)
        report_month_dt = first_day_of_month - datetime.timedelta(days=1)
        report_month = report_month_dt.month

    total_applications = AdmissionStudent.objects.order_by('-created').filter(
        created__year=date.year,
        created__month=report_month)

    # Online/offline applications
    online_applications = total_applications.filter(application_type='1')  # 1 is online
    offline_applications = total_applications.filter(application_type='2')

    total_admission = AdmissionStudent.objects.filter(admitted=True).filter(
        created__year=date.year,
        created__month=report_month)

    # Online/offline admissions
    total_admission_online = total_admission.filter(application_type='1')  # 1 is online
    total_admission_offline = total_admission.filter(application_type='2')  # 2 is offline

    # Report By Department
    departments = Department.objects.all()
    departmental_records = get_departments_record(departments, total_applications, total_admission)

    # Report by cities
    zila_records = get_active_cities_record(ALL_ZILA, total_applications, total_admission)

    ctx = {
        'date': datetime.date.today(),
        'report_month': report_month_dt.strftime('%B'),
        'total_applications': total_applications.count(),
        'total_admissions': total_admission.count(),
        'online_applications': online_applications.count(),
        'offline_applications': offline_applications.count(),
        'total_admission_online': total_admission_online.count(),
        'total_admission_offline': total_admission_offline.count(),
        'departmental_records': departmental_records,
        'zila_records': zila_records,
    }

    if response_type.lower() == 'json':
        return JsonResponse({'data': ctx})

    return render(request, 'students/reports/counsel_monthly_report.html', ctx)
