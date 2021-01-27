import datetime

from django.db.models.functions import ExtractMonth
from django.db.models import Count
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.template.loader import get_template

from students.models import AdmissionStudent
from academics.models import Department
from students.utils.bd_zila import ALL_ZILA
from students.utils.helpers import render_to_pdf


# Helper functions
def _get_departments_record(departments_qs, applications, admissions):
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
            'missed': applications.filter(department_choice=department, 
                                          rejected=True, admitted=False,
                                          paid=False).count(),
        }
    return departmental_records


def _get_active_cities_record(cities, applications, admissions):
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
        # Used for filtering qs
        report_month = date.month
        # Used to return reporting month name
        report_month_dt = date
    else:
        date = datetime.date.today()
        first_day_of_month = date.replace(day=1)
        # Used to return reporting month name
        report_month_dt = first_day_of_month - datetime.timedelta(days=1)
        # Used for filtering qs
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

    # Unpaid and rejected registrants
    # rejected applications are filtered out because they will not admit.
    unpaid_registrants = total_applications.filter(paid=False, rejected=False)
    rejected_registrants = total_applications.filter(rejected=True)

    # Report By Department
    departments = Department.objects.all()
    departmental_records = _get_departments_record(departments, total_applications, total_admission)

    # Report by cities
    zila_records = _get_active_cities_record(ALL_ZILA, total_applications, total_admission)

    ctx = {
        'date': datetime.date.today(),
        'report_month': report_month_dt.strftime('%B'), # Format full month name (July)
        'total_applications': total_applications.count(),
        'total_admissions': total_admission.count(),
        'online_applications': online_applications.count(),
        'offline_applications': offline_applications.count(),
        'total_admission_online': total_admission_online.count(),
        'total_admission_offline': total_admission_offline.count(),
        'unpaid_registrants': unpaid_registrants.count(),
        'rejected_registrants': rejected_registrants.count(),
        'departmental_records': departmental_records,
        'zila_records': zila_records,
    }

    if response_type.lower() == 'json':
        return JsonResponse({'data': ctx})
    elif response_type.lower() == 'pdf':
        template = get_template('students/reports/counsel_monthly_report.html')
        html = template.render(ctx)
        pdf = render_to_pdf(
            'students/reports/counsel_monthly_report.html', ctx)
        
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = 'counsel_report_%s' % (ctx.get('report_month'))
            content = f'inline; filename="{filename}"'
            # To download document as PDF
            download = request.GET.get('download')
            if download:
                content = f'attachment; filename="{filename}"'
            response['Content-Disposition'] = content
            return response
        return HttpResponse('Not found')

    return render(request, 'students/reports/counsel_monthly_report.html', ctx)


def yearly_graph_api(request):
    applications = AdmissionStudent.objects.annotate(
        month=ExtractMonth('created')).values('month').annotate(
            count=Count('id')).order_by('month')
    admissions = AdmissionStudent.objects.filter(
        admitted=True, paid=True).annotate(
        month=ExtractMonth('created')).values('month').annotate(
            count=Count('id')).order_by('month')
    pendings = AdmissionStudent.objects.filter(paid=False, admitted=False).annotate(
        month=ExtractMonth('created')).values('month').annotate(
            count=Count('id')).order_by('month')
    rejections = AdmissionStudent.objects.filter(rejected=True).annotate(
        month=ExtractMonth('created')).values('month').annotate(
            count=Count('id')).order_by('month')
    ctx = {
        'applications': list(applications),
        'admissions': list(admissions),
        'pendings': list(pendings),
        'rejections': list(rejections)
    }
    return JsonResponse({'data': ctx})
