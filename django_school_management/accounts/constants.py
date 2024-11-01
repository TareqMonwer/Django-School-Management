from enum import Enum


class ProfileApprovalStatusEnum(Enum):
    not_requested = 'n'
    pending = 'p'
    request_declined = 'd'
    approved = 'a'
