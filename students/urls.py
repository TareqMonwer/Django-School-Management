from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('all/', views.students_view, name='all_student'),
    path('add/', views.add_student_view, name='add_student'),
    path('update/<int:pk>/', views.student_update_view.as_view(),
         name='update_student'),
    path('<int:pk>/detail/', views.student_detail_view.as_view(),
         name='student_details'),
    path('<int:pk>/delete/', views.student_delete_view, name='delete_student'),
    path('<int:pk>/students/', views.students_by_department_view,
         name='students_by_dept'),

]
