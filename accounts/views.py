from rolepermissions.roles import assign_role
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView
from django.views.generic.edit import UpdateView
from django.urls import reverse

from academics.models import Department
from students.models import Student
from teachers.models import Teacher
from .forms import (
    UserRegistrationForm,
    ProfileCompleteForm,
    ApprovalProfileUpdateForm,
    UserChangeFormDashboard
)
from .models import CustomGroup, User
from .forms import (CommonUserProfileForm,
    UserProfileSocialLinksFormSet
)
from permission_handlers.administrative import (
    user_is_admin_or_su, user_editor_admin_or_su
)
from permission_handlers.basic import user_is_verified, permission_error


@login_required(login_url='account_login')
def profile_complete(request):
    ctx = {}
    user = User.objects.get(pk=request.user.pk)

    try:
        profile_edit_form = CommonUserProfileForm(
            instance=user.profile
        )
        social_links_form = UserProfileSocialLinksFormSet(
            instance=user.profile
        )
        ctx.update({
            'profile_edit_form': profile_edit_form,
            'social_links_form': social_links_form
        })
    except:
        messages.add_message(
            request,
            messages.INFO,
            "Maybe your account is not verified yet, please check your badge."
        )

    verification_form = ProfileCompleteForm(instance=user)
    if request.method == 'POST':
        verification_form = ProfileCompleteForm(
            request.POST,
            instance=user
        )
        if 'user-profile-update-form' in request.POST:
            profile_edit_form = CommonUserProfileForm(
                request.POST,
                request.FILES,
                instance=user.profile
            )
            social_links_form = UserProfileSocialLinksFormSet(
                request.POST,
                instance=user.profile
            )
            if profile_edit_form.is_valid():
                profile_edit_form.save()

            if social_links_form.is_valid():
                social_links_form.save()
            
            messages.add_message(
                request,
                messages.SUCCESS,
                'Your profile has been saved.'
            )
            return redirect('account:profile_complete')
        else:
            if verification_form.is_valid():
                verification_form.instance.approval_status = 'p'
                # approval status get's pending
                verification_form.save()
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    'Your request has been sent, please be patient.'
                )
                return redirect('account:profile_complete')
    user_permissions = user.user_permissions.all()
    ctx.update({
        'verification_form': verification_form,
        'user_perms': user_permissions if user_permissions else None,
    })
    return render(request, 'account/profile_complete.html', ctx)


@user_passes_test(
    user_editor_admin_or_su,
    login_url='account:profile_complete')
def dashboard(request):
    total_students = Student.objects.count()
    total_teachers = Teacher.objects.count()
    total_departments = Department.objects.count()
    context = {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_departments': total_departments,
    }
    return render(request, 'dashboard.html', context)


@user_passes_test(user_is_admin_or_su, login_url='account:permission_error')
def user_approval(request, pk, approved):
    """ Approve or decline approval request based on parameter `approved`.
    approved=0 means decline, 1 means approve.
    """
    user = User.objects.get(pk=pk)
    requested_role = user.requested_role

    if approved:
        assign_role(user, requested_role)
        if requested_role == 'admin':
            user.is_staff = True
        user.approval_status = 'a'
        user.save()
        messages.add_message(
            request,
            messages.SUCCESS,
            f'{user}\'s account has been approved.'
        )
    else:
        messages.add_message(
            request,
            messages.SUCCESS,
            f'{user}\'s request for {requested_role} has been declined.'
        )
    return redirect('account:user_requests')


@user_passes_test(user_is_admin_or_su, login_url='account:permission_error')
def user_approval_with_modification(request, pk):
    user = User.objects.get(pk=pk)
    form = ApprovalProfileUpdateForm()
    if request.method == 'POST':
        requested_role = request.POST.get('requested_role')
        assign_role(user, requested_role)
        if requested_role == 'admin':
            user.is_staff = True
        user.approval_status = 'a'
        user.save()
        messages.add_message(
            request,
            messages.SUCCESS,
            f'{user}\'s account has been approved.'
        )
        return redirect('account:user_requests')
    ctx = {
        'form': form,
    }
    return render(request, 'account/modify_approval.html', ctx)


# THIS IS ARCHIVED, SINCE WE'RE USING ALLAUTH
# def register(request):
#     if request.method == 'POST':
#         user_form = UserRegistrationForm(request.POST)
#         if user_form.is_valid():
#             new_user = user_form.save(commit=False)
#             new_user.set_password(
#                 user_form.cleaned_data['password1'])
#             new_user.save()
#             auth_user = authenticate(
#                 username=user_form.cleaned_data['username'],
#                 password=user_form.cleaned_data['password1']
#             )
#             if auth_user is not None:
#                 login(request, auth_user)
#             if auth_user.is_staff:
#                 return redirect('account:dashboard')
#             else:
#                 return redirect('account:profile_complete')
#         else:
#             return render(request, 'account/register.html', {'user_form': user_form})

#     else:
#         user_form = UserRegistrationForm()
#         return render(request, 'account/register.html', {'user_form': user_form})


class AccountListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = 'account/dashboard/accounts_list.html'
    context_object_name = 'accounts'

    def test_func(self):
        user =  self.request.user
        return user_is_verified(user)

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('account:profile_complete')
        return redirect('account_login')



class GroupListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = CustomGroup
    template_name = 'academics/group_list.html'
    context_object_name = 'groups'

    def test_func(self):
        user =  self.request.user
        return user_is_verified(user)

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('account:profile_complete')
        return redirect('account_login')


class UserRequestsListView(LoginRequiredMixin, UserPassesTestMixin,ListView):
    queryset = User.objects.exclude(approval_status='a')
    template_name = 'account/user_requests.html'
    context_object_name = 'users'

    def test_func(self):
        user =  self.request.user
        return user_is_admin_or_su(user)

user_requests_list = UserRequestsListView.as_view()


def profile_picture_upload(request):
    """
    Handles profile pic uploads coming through ajax.
    """
    if request.method == 'POST':
        image = request.FILES.get('profile-picture')
        try:
            request.user.profile.profile_picture = image
            request.user.profile.save()
            return JsonResponse({
                'status': 'ok',
                'imgUrl': request.user.profile.profile_picture.url,
            })
        except:
            return JsonResponse({'status': 'error'})


class UserUpdateView(UpdateView):
    form_class = UserChangeFormDashboard
    queryset = User.objects.all()
    template_name = 'account/dashboard/update_user.html'

    def get_success_url(self):
        return reverse(
            'articles:author_profile',
            args=[self.object.username,])