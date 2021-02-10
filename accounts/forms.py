from crispy_forms.helper import FormHelper

from django import forms as djform
from django.forms import inlineformset_factory
from django.contrib.auth import get_user_model, forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import CommonUserProfile, SocialLink

User = get_user_model()


class UserChangeForm(forms.UserChangeForm):
    class Meta(forms.UserChangeForm.Meta):
        model = User
        fields = ('requested_role', )


class UserChangeFormDashboard(forms.UserChangeForm):
    password = None
    
    class Meta(forms.UserChangeForm.Meta):
        model = User
        fields = (
            'username', 'email',
            'first_name', 'last_name',
            'requested_role', 'approval_status',
            'is_staff',
        )


class UserRegistrationForm(forms.UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.template_pack = 'tailwind'
    error_message = forms.UserCreationForm.error_messages.update(
        {
            "duplicate_username": _(
                "This username has already been taken."
            )
        }
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data["username"]

        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username

        raise ValidationError(
            self.error_messages["duplicate_username"]
        )

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Password didn\'t match!')
        return cd['password2']


class ProfileCompleteForm(djform.ModelForm):
    class Meta:
        model = User
        fields = [
            'employee_or_student_id',
            'requested_role',
            'email',
            'approval_extra_note']


class ApprovalProfileUpdateForm(djform.ModelForm):
    class Meta:
        model = User
        fields = ['requested_role']


UserProfileSocialLinksFormSet = inlineformset_factory(
    CommonUserProfile, SocialLink,
    fields=('media_name', 'url'),
    extra=4,
    max_num=4
)

class CommonUserProfileForm(djform.ModelForm):
    class Meta:
        model = CommonUserProfile
        fields = [
            'profile_picture',
            'cover_picture',
            'headline',
            'show_headline_in_bio',
            'country',
            'summary'
        ]