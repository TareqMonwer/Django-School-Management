from enum import Enum


class AcademicsURLEnum(Enum):
    all_semester = 'semesters/'
    departments = 'departments/'
    create_department = 'create-department/'
    create_semester = 'create-semester/'
    create_academic_session = 'create-academic-session/'
    create_subject = 'create-subject'
    delete_dept = 'depts/delete/<int:pk>/'
    academic_sessions = 'academic_sessions/'
    update_department = 'department/update/<int:pk>/'
    subject_list = 'subjects/'
    import_subject_csv = 'upload-subjects-csv/'


class AcademicsURLConstants:
    all_semester = f'academics:{AcademicsURLEnum.all_semester.name}'
    departments = f'academics:{AcademicsURLEnum.departments.name}'
    create_department = f'academics:{AcademicsURLEnum.create_department.name}'
    create_semester = f'academics:{AcademicsURLEnum.create_semester.name}'
    create_academic_session = f'academics:{AcademicsURLEnum.create_academic_session.name}'
    create_subject = f'academics:{AcademicsURLEnum.create_subject.name}'
    delete_dept = f'academics:{AcademicsURLEnum.delete_dept.name}'
    academic_sessions = f'academics:{AcademicsURLEnum.academic_sessions.name}'
    update_department = f'academics:{AcademicsURLEnum.update_department.name}'
    subject_list = f'academics:{AcademicsURLEnum.subject_list.name}'
    import_subject_csv = f'academics:{AcademicsURLEnum.import_subject_csv.name}'
