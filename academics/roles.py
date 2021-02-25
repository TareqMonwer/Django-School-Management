from rolepermissions.roles import AbstractUserRole

class Subscriber(AbstractUserRole):
    available_permissions = {
        'visit_website': True,
    }

class Student(AbstractUserRole):
    available_permissions = {
        'view_result': True,
        'create_article': True,
        'add_testimonial': True,
        'can_see_dashboard': True
    }
    # Student has all perms that a subscriber has.
    available_permissions.update(Subscriber.available_permissions)


class Teacher(AbstractUserRole):
    available_permissions = {
        'add_result': True,
        'update_result': True,
    }
    available_permissions.update(Student.available_permissions)


class Editor(AbstractUserRole):
    available_permissions = {
        'crud_teacher_application': True,
        'crud_student_application': True,
        'crud_subject': True,
        'crud_academic_session': True,
        'crud_designation': True,
        'crud_result': True,
    }
    available_permissions.update(Teacher.available_permissions)


class AcademicOficer(AbstractUserRole):
    available_permissions = {
        'crud_academic_session': True,
        'crud_counsel': True,
    }
    available_permissions.update(Editor.available_permissions)


class Admin(AbstractUserRole):
    available_permissions = {
        'crud_users': True,
    }
    available_permissions.update(AcademicOficer.available_permissions)


# Note: Accounts will have a bit different 
# set of perms, they shouldn't be involved in 
# any other actions.
class Accounts(AbstractUserRole):
    available_permissions = {
        'manipulate_payments': True,
    }
    available_permissions.update(Student.available_permissions)