from rolepermissions.roles import AbstractUserRole

class Admin(AbstractUserRole):
    available_permissions = {
        'create_stuff': True,
        'create_teacher': True,
    }

class Stuff(AbstractUserRole):
    available_permissions = {
        'create_teacher': True,
    }
