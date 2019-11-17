from django.shortcuts import render
from django.contrib.auth import authenticate, login

from .forms import UserRegistrationForm


def dashboard(request):
    return render(request, 'account/registration_done.html')


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password'])
            new_user.save()
            auth_user = authenticate(username=user_form.cleaned_data['username'],
                                     password=user_form.cleaned_data['password'])
            if auth_user is not None:
                login(request, auth_user)
            return render(request, 'account/registration_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
        return render(request, 'account/register.html', {'user_form': user_form})
