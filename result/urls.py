from django.urls import path

from . import views

app_name = 'result'

urlpatterns = [
    path('', views.result_view, name='result_home'),
    path('create-subject-group/', views.create_subject_group,
        name='create_subject_group'
    ),
    path('subject-groups/', views.subject_group_list, name='subject_groups'),
    path('student/<int:student_pk>/', views.result_detail_view,
        name='result_detail_view'
    ),
    path('entry/', views.result_entry,
        name='result_entry'
    ),
    path('student/find/<str:student_id>', views.find_student,
        name='find_student'
    ),
]
