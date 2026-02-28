from datetime import datetime

from django.urls import path, register_converter

from django_school_management.students.constants import StudentsURLEnums

from .views import students_views as views
from .views import pdf_views
from .views import report_views

app_name = "students"


class DateConverter:
    # Convert a string passed as date in datetime object
    regex = "\d{4}-\d{2}-\d{2}"

    def to_python(self, value):
        return datetime.strptime(value, "%Y-%m-%d")

    def to_url(self, value):
        return value


register_converter(DateConverter, "date")

urlpatterns = [
    path(
        StudentsURLEnums.students_dashboard_index.value,
        views.students_dashboard_index,
        name=StudentsURLEnums.students_dashboard_index.name,
    ),
    # TEST PDF PRINTER
    path(
        StudentsURLEnums.test_pdf.value,
        pdf_views.test_pdf,
        name=StudentsURLEnums.test_pdf.name,
    ),
    path(
        StudentsURLEnums.add_student.value,
        views.add_student_view,
        name=StudentsURLEnums.add_student.name,
    ),
    path(
        StudentsURLEnums.all_student.value,
        views.students_view,
        name=StudentsURLEnums.all_student.name,
    ),
    path(
        StudentsURLEnums.alumnus.value,
        views.AlumnusListView.as_view(),
        name=StudentsURLEnums.alumnus.name,
    ),
    path(
        StudentsURLEnums.all_applicants.value,
        views.all_applicants,
        name=StudentsURLEnums.all_applicants.name,
    ),
    path(
        StudentsURLEnums.unpaid_registrants.value,
        views.unpaid_registrants,
        name=StudentsURLEnums.unpaid_registrants.name,
    ),
    path(
        StudentsURLEnums.mark_as_paid_or_unpaid.value,
        views.mark_as_paid_or_unpaid,
        name=StudentsURLEnums.mark_as_paid_or_unpaid.name,
    ),
    path(
        StudentsURLEnums.add_counseling_data.value,
        views.add_counseling_data,
        name=StudentsURLEnums.add_counseling_data.name,
    ),
    path(
        StudentsURLEnums.admitted_student_list.value,
        views.admitted_students_list,
        name=StudentsURLEnums.admitted_student_list.name,
    ),
    path(
        StudentsURLEnums.admission_confirmation.value,
        views.admission_confirmation,
        name=StudentsURLEnums.admission_confirmation.name,
    ),
    path(
        StudentsURLEnums.get_json_batch_data.value,
        views.get_json_batch_data,
        name=StudentsURLEnums.get_json_batch_data.name,
    ),
    path(
        StudentsURLEnums.yearly_graph_api.value,
        report_views.yearly_graph_api,
        name=StudentsURLEnums.yearly_graph_api.name,
    ),
    path(
        StudentsURLEnums.admit_student.value,
        views.admit_student,
        name=StudentsURLEnums.admit_student.name,
    ),
    path(
        StudentsURLEnums.paid_registrants.value,
        views.paid_registrants,
        name=StudentsURLEnums.paid_registrants.name,
    ),
    path(
        StudentsURLEnums.rejected_registrants.value,
        views.rejected_registrants,
        name=StudentsURLEnums.rejected_registrants.name,
    ),
    path(
        StudentsURLEnums.update_online_registrant.value,
        views.update_online_registrant,
        name=StudentsURLEnums.update_online_registrant.name,
    ),
    path(
        StudentsURLEnums.update_student.value,
        views.StudentUpdateView.as_view(),
        name=StudentsURLEnums.update_student.name,
    ),
    path(
        StudentsURLEnums.student_details.value,
        views.StudentDetailsView.as_view(),
        name=StudentsURLEnums.student_details.name,
    ),
    path(
        StudentsURLEnums.student_sis.value,
        views.StudentSISView.as_view(),
        name=StudentsURLEnums.student_sis.name,
    ),
    path(
        StudentsURLEnums.delete_student.value,
        views.student_delete_view,
        name=StudentsURLEnums.delete_student.name,
    ),
    path(
        StudentsURLEnums.students_by_dept.value,
        views.students_by_department_view,
        name=StudentsURLEnums.students_by_dept.name,
    ),
    path(
        StudentsURLEnums.counsel_monthly_report.value,
        report_views.counsel_monthly_report,
        name=StudentsURLEnums.counsel_monthly_report.name,
    ),
    path(
        StudentsURLEnums.counsel_monthly_report_typed.value,
        report_views.counsel_monthly_report,
        name=StudentsURLEnums.counsel_monthly_report_typed.name,
    ),
    path(
        StudentsURLEnums.counsel_report_monthly_with_date.value,
        report_views.counsel_monthly_report,
        name=StudentsURLEnums.counsel_report_monthly_with_date.name,
    ),
    path(
        StudentsURLEnums.student_my_portal.value,
        views.student_my_portal,
        name=StudentsURLEnums.student_my_portal.name,
    ),
    path(
        StudentsURLEnums.reject_applicant.value,
        views.reject_applicant,
        name=StudentsURLEnums.reject_applicant.name,
    ),
]
