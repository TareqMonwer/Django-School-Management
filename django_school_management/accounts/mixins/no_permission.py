from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

from django_school_management.accounts.constants import AccountURLConstants


class LoginRequiredNoPermissionMixin(LoginRequiredMixin):
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect(AccountURLConstants.profile_complete)
        return redirect('account_login')