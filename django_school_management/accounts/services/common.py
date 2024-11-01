from django_school_management.accounts.constants import ProfileApprovalStatusEnum
from django_school_management.accounts.models import User


def profile_not_approved(user: User) -> bool:
    return user.approval_status != ProfileApprovalStatusEnum.approved.value


def map_profile_approval_status_message(approval_status: str) -> str:
    messages = {
        ProfileApprovalStatusEnum.approved.value: 'Your account is approved.',
        ProfileApprovalStatusEnum.not_requested.value: 'Please request for profile approval with appropriate reason.',
        ProfileApprovalStatusEnum.pending.value: 'Please wait, your request for approval is pending.',
        ProfileApprovalStatusEnum.request_declined.value: 'Your request has been declined, apply again with appropriate reason.',
    }
    return messages[approval_status]
