from django.urls import path
from . import views
from .constants import AcademicsURLEnum

app_name = 'academics'

urlpatterns = [
    # Semester
    path(
        AcademicsURLEnum.all_semester.name,
        views.semesters,
        name=AcademicsURLEnum.all_semester.value
    ),
    path(
        AcademicsURLEnum.departments.name,
        views.departments,
        name=AcademicsURLEnum.departments.value
    ),
    path(
        AcademicsURLEnum.create_department.name,
        views.create_department,
        name=AcademicsURLEnum.create_department.value
    ),
    path(
        AcademicsURLEnum.create_semester.name,
        views.create_semester,
        name=AcademicsURLEnum.create_semester.value
    ),
    path(
        AcademicsURLEnum.create_academic_session.name,
        views.create_academic_semester,
        name=AcademicsURLEnum.create_academic_session.value
    ),
    path(
        AcademicsURLEnum.create_subject.name,
        views.create_subject,
        name=AcademicsURLEnum.create_subject.value
    ),
    path(
        AcademicsURLEnum.delete_dept.name,
        views.delete_department,
        name=AcademicsURLEnum.delete_dept.value
    ),
    path(
        AcademicsURLEnum.academic_sessions.name,
        views.academic_session,
        name=AcademicsURLEnum.academic_sessions.value
    ),
    path(
        AcademicsURLEnum.update_department.name,
        views.UpdateDepartment.as_view(),
        name=AcademicsURLEnum.update_department.value
    ),
    path(
        AcademicsURLEnum.subject_list.name,
        views.subject_list,
        name=AcademicsURLEnum.subject_list.value
    ),
    path(
        AcademicsURLEnum.import_subject_csv.name,
        views.upload_subjects_csv,
        name=AcademicsURLEnum.import_subject_csv.value
    ),
]
