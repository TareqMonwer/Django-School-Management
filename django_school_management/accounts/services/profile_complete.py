from typing import Any

from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import redirect

from django_school_management.accounts.forms import CommonUserProfileForm, UserProfileSocialLinksFormSet, \
    ProfileCompleteForm
from django_school_management.accounts.models import User


class ProfileCompleteService:
    def __init__(self, request: WSGIRequest, user: User, session_messages):
        self.request = request
        self.user = user
        self.session_messages = session_messages

    def _handle_user_profile_update(self) -> None:
        profile_edit_form = CommonUserProfileForm(
            self.request.POST,
            self.request.FILES,
            instance=self.user.profile
        )
        social_links_form = UserProfileSocialLinksFormSet(
            self.request.POST,
            instance=self.user.profile
        )
        if profile_edit_form.is_valid():
            profile_edit_form.save()

        if social_links_form.is_valid():
            social_links_form.save()

        self.session_messages.add_message(
            self.request,
            self.session_messages.SUCCESS,
            'Your profile has been saved.'
        )

    def _handle_handle_approval_submit(self) -> None:
        verification_form = ProfileCompleteForm(
            self.request.POST,
            instance=self.user
        )

        if verification_form.is_valid():
            verification_form.instance.approval_status = 'p'
            # approval status get's pending
            verification_form.save()
            self.session_messages.add_message(
                self.request,
                self.session_messages.SUCCESS,
                'Your request has been sent. I will be approved by your institute.'
            )

    @staticmethod
    def handle_profile_update(self):
        if 'user-profile-update-form' in self.request.POST:
            self._handle_handle_approval_submit()
        else:
            self._handle_user_profile_update()

        return redirect('account:profile_complete')