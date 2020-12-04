from django.urls import path
from .views import students_views as views
from .views import pdf_views
from .views import report_views

app_name = 'students'

urlpatterns = [
     path('', views.students_dashboard_index, 
          name='students_dashboard_index'),
     path('add/', views.add_student_view, name='add_student'),
     path('all/', views.students_view, name='all_student'),
     path('applicants/', views.all_applicants, name='all_applicants'),
     path('applicants/unpaid/', views.unpaid_registrants, name='unpaid_registrants'),
     path('applicants/unpaid/mark-paid/', views.mark_as_paid_or_unpaid, name='mark_as_paid_or_unpaid'),
     path('add-counsel-data/<int:student_id>/', views.add_counseling_data, 
          name='add_counseling_data'),
     path('admitted-students/', views.admitted_students_list,
          name='admitted_student_list'),
     path('online-applicants/<int:pk>/admit/', views.admit_student,
          name='admit_student'),
     path('paid-registrants/', views.paid_registrants, 
          name='paid_registrants'),
     path('update-registrant/<int:pk>/', views.update_online_registrant, 
          name='update_online_registrant'),
     path('update/<int:pk>/', views.student_update_view.as_view(),
          name='update_student'),
     path('<int:pk>/detail/', views.student_detail_view.as_view(),
          name='student_details'),
     path('<int:pk>/delete/', views.student_delete_view, name='delete_student'),
     path('<int:pk>/students/', views.students_by_department_view,
          name='students_by_dept'),
     path('result/', views.student_result_view, name='result'),
     path('add_result_from_student/<int:pk>/', views.add_result_from_student_detail_view, 
          name='add_result_in_details'),
     path('pdf/', pdf_views.test_pdf, name='test_pdf'),
     path('counsel-report/', report_views.counsel_monthly_report, name='counsel_monthly_report'),
]
