from django.urls import path
from . import views
from account.views import AccountListView


app_name = 'academics'

urlpatterns = [
    # Semester
    path('semesters/', views.semesters, name='all_semester'),
    path('departments/', views.departments, name='departments'),
    path('depts/delete/<int:pk>/', views.delete_department, name='delete_dept'),
    path('academic_sessions/', views.academic_session, name='academic_sessions'),
    path('add_user/', views.add_user_view, name='add_user'),
    path('accounts/', AccountListView.as_view(), name='all_accounts'),
    path('department/update/<int:pk>/', views.UpdateDepartment.as_view(),
        name='update_department'),
]
