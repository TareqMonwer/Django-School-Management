from enum import Enum


class TeachersURLEnums(Enum):
    all_teacher = 'all/'
    add_teacher = 'add/'
    teacher_details = '<int:pk>/details/'
    update_teacher = '<int:pk>/update/'
    delete_teacher = '<int:pk>/delete/'
    designations = 'designations/'
    create_designation = 'create/designation/'
    teacher_my_portal = "my-portal/<str:teacher_id>/"


class TeachersURLConstants:
    all_teacher = f"teachers:{TeachersURLEnums.all_teacher.name}"
    add_teacher = f"teachers:{TeachersURLEnums.add_teacher.name}"
    teacher_details = f"teachers:{TeachersURLEnums.teacher_details.name}"
    update_teacher = f"teachers:{TeachersURLEnums.update_teacher.name}"
    delete_teacher = f"teachers:{TeachersURLEnums.delete_teacher.name}"
    designations = f"teachers:{TeachersURLEnums.designations.name}"
    create_designation = f"teachers:{TeachersURLEnums.create_designation.name}"
    teacher_my_portal = f"teachers:{TeachersURLEnums.teacher_my_portal.name}"
