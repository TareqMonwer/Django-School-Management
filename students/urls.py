from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
     path('', views.students_dashboard_index, 
          name='students_dashboard_index'),
     path('all/', views.students_view, name='all_student'),
     path('add/', views.add_student_view, name='add_student'),
     path('online-applicants/', views.online_applicants_list, 
          name='online_applicants_list'),
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
]
