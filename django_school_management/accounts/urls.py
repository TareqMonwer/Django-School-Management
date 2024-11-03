from permission_handlers.basic import permission_error
from django.urls import path, include
from . import views
from .constants import AccountURLEnums

app_name = 'account'

urlpatterns = [
    path(
        AccountURLEnums.profile_complete.value,
        views.profile_complete,
        name=AccountURLEnums.profile_complete.name
    ),
    path('auth/', include('django.contrib.auth.urls')),
    path(
        AccountURLEnums.dashboard.value,
        views.dashboard,
        name=AccountURLEnums.dashboard.name
    ),
    path(
        AccountURLEnums.groups.value,
        views.GroupListView.as_view(),
        name=AccountURLEnums.groups.name
    ),
    path(
        AccountURLEnums.user_requests.value,
        views.user_requests_list,
        name=AccountURLEnums.user_requests.name
    ),
    path(
        AccountURLEnums.permission_error.value,
        permission_error,
        name=AccountURLEnums.permission_error.name
    ),
    path(
        AccountURLEnums.user_approval.value,
        views.user_approval,
        name=AccountURLEnums.user_approval.name
    ),
    path(
        AccountURLEnums.approval_with_modification.value,
        views.user_approval_with_modification,
        name=AccountURLEnums.approval_with_modification.name
    ),
    path(
        AccountURLEnums.user_change.value,
        views.UserUpdateView.as_view(),
        name=AccountURLEnums.user_change.name
    ),
    path(
        AccountURLEnums.profile_picture_upload.value,
        views.profile_picture_upload,
        name=AccountURLEnums.profile_picture_upload.name
    ),
    path(
        AccountURLEnums.all_accounts.value,
        views.AccountListView.as_view(),
        name=AccountURLEnums.all_accounts.name
    ),
    path(
        AccountURLEnums.add_user.value,
        views.add_user_view,
        name=AccountURLEnums.add_user.name
    ),
]
