from django.urls import path
from . import views
from accounts.views import AccountListView


app_name = 'academics'

urlpatterns = [
    # Semester
    path('semesters/', views.semesters, name='all_semester'),
    path('departments/', views.departments, name='departments'),
    path('create-department/', views.create_department,
        name='create_department'
    ),
    path('create-semester/', views.create_semester,
        name='create_semester'
    ),
    path('create-academic-session/', views.create_academic_semester,
        name='create_academic_session'
    ),
    path('create-subject', views.create_subject,
        name='create_subject'
    ),
    path('depts/delete/<int:pk>/', views.delete_department, name='delete_dept'),
    path('academic_sessions/', views.academic_session, name='academic_sessions'),
    path('add_user/', views.add_user_view, name='add_user'),
    path('accounts/', AccountListView.as_view(), name='all_accounts'),
    path('department/update/<int:pk>/', views.UpdateDepartment.as_view(),
        name='update_department'),
    path('subjects/', views.subject_list, name='subject_list'),
    path('upload-subjects-csv/', views.upload_subjects_csv, name='import_subject_csv'),
]
