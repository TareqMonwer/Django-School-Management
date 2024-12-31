from django_school_management.students.constants import StudentsURLConstants
from django_school_management.teachers.constants import TeachersURLConstants


all_teachers = dict(name=TeachersURLConstants.all_teacher, title="Teachers")
articles_manage = dict(name="articles:dashboard_manage", title="Articles")
teacher_designations = dict(name=TeachersURLConstants.designations, title="Designations")
write_article = dict(
    name="articles:publish_article_from_dashboard",
    title="Write Article",
)

add_student = {
    "name": StudentsURLConstants.add_student,
    "title": "New Application",
}
all_students = {"name": StudentsURLConstants.all_student, "title": "Students List"}
add_result = {"name": "result:result_entry", "title": "Add Result"}
results_index = {"name": "result:result_home", "title": "Results"}
alumnus = {"name": StudentsURLConstants.alumnus, "title": "Alumnus"}

MENU_CONFIG = {
    "student": [
        {
            "groups": {"teacher", "admin"},
            "urls": [
                all_students,
                add_result,
            ],
        },
        {
            "groups": {"student", "teacher", "admin"},
            "urls": [
                results_index,
                alumnus,
            ],
        },
        {
            "groups": {"academic_officer"},
            "urls": [
                add_student,
                all_students,
                alumnus,
            ],
        },
    ],
    "teacher": [
        {
            "groups": {"teacher", "admin"},
            "urls": [
                write_article,
                all_teachers,
            ],
        },
        {
            "groups": {"student"},
            "urls": [all_teachers],
        },
        {
            "groups": {"editor"},
            "urls": [
                all_teachers,
                articles_manage,
                write_article,
            ],
        },
        {
            "groups": {"academic_officer"},
            "urls": [all_teachers],
        },
        {
            "groups": {"admin"},
            "urls": [teacher_designations],
        },
    ],
}
