from django.urls import path
from . import views
from .constants import AcademicsURLEnum

app_name = 'academics'

urlpatterns = [
    path(AcademicsURLEnum.batch_list.value, views.batch_list_view, name=AcademicsURLEnum.batch_list.name),
    path(AcademicsURLEnum.create_batch.value, views.create_batch_view, name=AcademicsURLEnum.create_batch.name),
    path(AcademicsURLEnum.all_semester.value, views.semesters, name=AcademicsURLEnum.all_semester.name),
    path(AcademicsURLEnum.departments.value, views.departments, name=AcademicsURLEnum.departments.name),
    path(AcademicsURLEnum.create_department.value, views.create_department, name=AcademicsURLEnum.create_department.name),
    path(AcademicsURLEnum.create_semester.value, views.create_semester, name=AcademicsURLEnum.create_semester.name),
    path(AcademicsURLEnum.create_academic_session.value, views.create_academic_semester, name=AcademicsURLEnum.create_academic_session.name),
    path(AcademicsURLEnum.create_subject.value, views.create_subject, name=AcademicsURLEnum.create_subject.name),
    path(AcademicsURLEnum.delete_dept.value, views.delete_department, name=AcademicsURLEnum.delete_dept.name),
    path(AcademicsURLEnum.academic_sessions.value, views.academic_session, name=AcademicsURLEnum.academic_sessions.name),
    path(AcademicsURLEnum.update_department.value, views.UpdateDepartment.as_view(), name=AcademicsURLEnum.update_department.name),
    path(AcademicsURLEnum.subject_list.value, views.subject_list, name=AcademicsURLEnum.subject_list.name),
    path(AcademicsURLEnum.import_subject_csv.value, views.upload_subjects_csv, name=AcademicsURLEnum.import_subject_csv.name),
    # Subject update/delete
    path(AcademicsURLEnum.update_subject.value, views.update_subject, name=AcademicsURLEnum.update_subject.name),
    path(AcademicsURLEnum.delete_subject.value, views.delete_subject, name=AcademicsURLEnum.delete_subject.name),
    # Academic Session update/delete
    path(AcademicsURLEnum.update_academic_session.value, views.update_academic_session, name=AcademicsURLEnum.update_academic_session.name),
    path(AcademicsURLEnum.delete_academic_session.value, views.delete_academic_session, name=AcademicsURLEnum.delete_academic_session.name),
    # Batch update/delete
    path(AcademicsURLEnum.update_batch.value, views.update_batch, name=AcademicsURLEnum.update_batch.name),
    path(AcademicsURLEnum.delete_batch.value, views.delete_batch, name=AcademicsURLEnum.delete_batch.name),
    # Semester update/delete
    path(AcademicsURLEnum.update_semester.value, views.update_semester, name=AcademicsURLEnum.update_semester.name),
    path(AcademicsURLEnum.delete_semester.value, views.delete_semester, name=AcademicsURLEnum.delete_semester.name),
]
