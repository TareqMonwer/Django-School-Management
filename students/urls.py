from datetime import datetime
from django.urls import path, register_converter
from .views import students_views as views
from .views import pdf_views
from .views import report_views

app_name = 'students'


class DateConverter:
     # Convert a string passed as date in datetime object
     regex = '\d{4}-\d{2}-\d{2}'

     def to_python(self, value):
          return datetime.strptime(value, '%Y-%m-%d')
     
     def to_url(self, value):
          return value

register_converter(DateConverter, 'date')

urlpatterns = [
     path('', views.students_dashboard_index, 
          name='students_dashboard_index'),
     # TEST PDF PRINTER
     path('pdf/', pdf_views.test_pdf, name='test_pdf'),
     path('add/', views.add_student_view, name='add_student'),
     path('all/', views.students_view, name='all_student'),
     path('applicants/', views.all_applicants, name='all_applicants'),
     path('applicants/unpaid/', views.unpaid_registrants, name='unpaid_registrants'),
     path('applicants/unpaid/mark-paid/', views.mark_as_paid_or_unpaid,
          name='mark_as_paid_or_unpaid'),
     path('add-counsel-data/<int:student_id>/', views.add_counseling_data, 
          name='add_counseling_data'),
     path('admitted-students/', views.admitted_students_list,
          name='admitted_student_list'),
     path('admission-confirm/', views.admission_confirmation,
          name='admission_confirmation'),
     path('api/batches/<int:department_code>/', views.get_json_batch_data,
          name='get_json_batch_data'),
     path('api/yearly-graph/', report_views.yearly_graph_api,
          name='yearly_graph_api'),
     path('online-applicants/<int:pk>/admit/', views.admit_student,
          name='admit_student'),
     path('paid-registrants/', views.paid_registrants, 
          name='paid_registrants'),
     path('rejected-registrants/', views.rejected_registrants,
          name='rejected_registrants'),
     path('update-registrant/<int:pk>/', views.update_online_registrant, 
          name='update_online_registrant'),
     path('update/<int:pk>/', views.student_update_view.as_view(),
          name='update_student'),
     path('<int:pk>/detail/', views.student_detail_view.as_view(),
          name='student_details'),
     path('<int:pk>/delete/', views.student_delete_view, name='delete_student'),
     path('<int:pk>/students/', views.students_by_department_view,
          name='students_by_dept'),
     path('counsel-report/', report_views.counsel_monthly_report, name='counsel_monthly_report'),
     path('counsel-report/<str:response_type>/', report_views.counsel_monthly_report,
          name='counsel_monthly_report_typed'),
     path('counsel-report/<str:response_type>/<date:date_param>/',
          report_views.counsel_monthly_report,
          name='counsel_report_monthly_with_date'),
]
