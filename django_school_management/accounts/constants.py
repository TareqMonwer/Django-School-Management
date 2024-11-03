from enum import Enum


class ProfileApprovalStatusEnum(Enum):
    not_requested = 'n'
    pending = 'p'
    request_declined = 'd'
    approved = 'a'


class AccountTypesEnum(Enum):
    subscriber = 'subscriber'
    student = 'student'
    teacher = 'teacher'
    editor = 'editor'
    academic_officer = 'academic_officer'
    admin = 'admin'


class AccountURLEnums(Enum):
    all_accounts = 'accounts/'
    add_user = 'add_user/'
    approval_with_modification = 'modify-and-approve/<int:pk>/'
    dashboard = 'dashboard/'
    groups = 'groups/'
    permission_error = 'permission-error/'
    profile_picture_upload = 'api/upload-profile-picture'
    user_change = 'user/<int:pk>/change'
    user_requests = 'user-requests/'
    user_approval = 'approval/<int:pk>/<int:approved>'
    profile_complete = ''


class AccountURLConstants:
    all_accounts = f'account:{AccountURLEnums.all_accounts.name}'
    add_user = f'account:{AccountURLEnums.add_user.name}'
    approval_with_modification = f'account:{AccountURLEnums.approval_with_modification.name}'
    dashboard = f'account:{AccountURLEnums.dashboard.name}'
    groups = f'account:{AccountURLEnums.groups.name}'
    permission_error = f'account:{AccountURLEnums.permission_error.name}'
    profile_picture_upload = f'account:{AccountURLEnums.profile_picture_upload.name}'
    user_change = f'account:{AccountURLEnums.user_change.name}'
    user_requests = f'account:{AccountURLEnums.user_requests.name}'
    user_approval = f'account:{AccountURLEnums.user_approval.name}'
    profile_complete = f'account:{AccountURLEnums.profile_complete.name}'
