from django.urls import path

from django_school_management.teachers.constants import TeachersURLEnums
from . import views


app_name = "teachers"

urlpatterns = [
    path(
        TeachersURLEnums.all_teacher.value,
        views.teachers_view,
        name=TeachersURLEnums.all_teacher.name,
    ),
    path(
        TeachersURLEnums.add_teacher.value,
        views.add_teacher_view,
        name=TeachersURLEnums.add_teacher.value,
    ),
    path(
        TeachersURLEnums.teacher_details.value,
        views.teacher_detail_view,
        name=TeachersURLEnums.teacher_details.name,
    ),
    path(
        TeachersURLEnums.update_teacher.value,
        views.teacher_update_view.as_view(),
        name=TeachersURLEnums.update_teacher.name,
    ),
    path(
        TeachersURLEnums.delete_teacher.value,
        views.teacher_delete_view,
        name=TeachersURLEnums.delete_teacher.name,
    ),
    path(
        TeachersURLEnums.designations.value,
        views.designation_list_view.as_view(),
        name=TeachersURLEnums.designations.name,
    ),
    path(
        TeachersURLEnums.create_designation.value,
        views.create_designation,
        name=TeachersURLEnums.create_designation.name,
    ),
]
