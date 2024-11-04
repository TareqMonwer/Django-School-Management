from django.urls import path
from . import views
from .constants import AcademicsURLEnum

app_name = 'academics'

urlpatterns = [
    # Semester
    path(
        AcademicsURLEnum.all_semester.value,
        views.semesters,
        name=AcademicsURLEnum.all_semester.name
    ),
    path(
        AcademicsURLEnum.departments.value,
        views.departments,
        name=AcademicsURLEnum.departments.name
    ),
    path(
        AcademicsURLEnum.create_department.value,
        views.create_department,
        name=AcademicsURLEnum.create_department.name
    ),
    path(
        AcademicsURLEnum.create_semester.value,
        views.create_semester,
        name=AcademicsURLEnum.create_semester.name
    ),
    path(
        AcademicsURLEnum.create_academic_session.value,
        views.create_academic_semester,
        name=AcademicsURLEnum.create_academic_session.name
    ),
    path(
        AcademicsURLEnum.create_subject.value,
        views.create_subject,
        name=AcademicsURLEnum.create_subject.name
    ),
    path(
        AcademicsURLEnum.delete_dept.value,
        views.delete_department,
        name=AcademicsURLEnum.delete_dept.name
    ),
    path(
        AcademicsURLEnum.academic_sessions.value,
        views.academic_session,
        name=AcademicsURLEnum.academic_sessions.name
    ),
    path(
        AcademicsURLEnum.update_department.value,
        views.UpdateDepartment.as_view(),
        name=AcademicsURLEnum.update_department.name
    ),
    path(
        AcademicsURLEnum.subject_list.value,
        views.subject_list,
        name=AcademicsURLEnum.subject_list.name
    ),
    path(
        AcademicsURLEnum.import_subject_csv.value,
        views.upload_subjects_csv,
        name=AcademicsURLEnum.import_subject_csv.name
    ),
]
