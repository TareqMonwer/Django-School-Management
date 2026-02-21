from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.db import models
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView

from django_school_management.academics.models import Department, AcademicSession
from django_school_management.institute.forms.institute_profile_form import InstituteProfileCreateForm
from django_school_management.institute.forms.onboarding_forms import (
    OnboardingStep1Form,
    OnboardingDepartmentFormSet,
    OnboardingAcademicSessionForm,
)
from .models import InstituteProfile


# ──────────────────────────────────────────────
# Existing config views (kept for settings pages)
# ──────────────────────────────────────────────

class InstituteProfileConfigListView(ListView):
    model = InstituteProfile
    context_object_name = 'institute_profiles'
    template_name = 'institute/dashboard/institute_profile_list.html'


class InstituteProfileConfigDashboard(UpdateView):
    model = InstituteProfile
    fields = '__all__'
    pk_url_kwarg = 'institute_pk'
    template_name = 'institute/dashboard/config_form.html'


class InstituteProfileSetupDashboard(CreateView):
    model = InstituteProfile
    form_class = InstituteProfileCreateForm
    template_name = 'institute/dashboard/config_form.html'

    def dispatch(self, request, *args, **kwargs):
        if InstituteProfile.objects.filter(active=True).exists():
            return redirect('institute:onboarding_step1')
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_success_url(self) -> str:
        institute = InstituteProfile.objects.get(active=True)
        return reverse_lazy('institute:institute_detail', kwargs={'institute_pk': institute.pk})


class InstituteProfileDetailDashboard(DetailView):
    model = InstituteProfile
    pk_url_kwarg = 'institute_pk'
    template_name = 'institute/dashboard/config.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        institute_fields = serializers.serialize("python", InstituteProfile.objects.all())
        ctx['institute_fields'] = institute_fields
        return ctx


class SetActiveInstituteProfile(View):
    def get(self, request, institute_pk, *args, **kwargs):
        institute = InstituteProfile.objects.get(pk=institute_pk)
        institute.active = True
        institute.save()
        return redirect('institute:institute_detail', institute_pk)


# ──────────────────────────────────────────────
# Onboarding Wizard
# ──────────────────────────────────────────────

ONBOARDING_STEPS = [
    {'number': 1, 'title': 'School Profile', 'icon': 'fas fa-school'},
    {'number': 2, 'title': 'Academics', 'icon': 'fas fa-graduation-cap'},
    {'number': 3, 'title': 'Review & Launch', 'icon': 'fas fa-rocket'},
]


def _onboarding_context(current_step):
    steps = []
    for s in ONBOARDING_STEPS:
        steps.append({
            **s,
            'status': 'completed' if s['number'] < current_step
            else 'active' if s['number'] == current_step
            else 'upcoming',
        })
    return {'onboarding_steps': steps, 'current_step': current_step}


def _resolve_institute(user):
    """Find the institute for this user, checking:
    1. The user's linked institute
    2. The active institute in the DB (legacy / pre-existing)
    If found via (2), link it to the user so subsequent lookups are fast.
    """
    institute = getattr(user, 'institute', None)
    if institute:
        return institute

    active = InstituteProfile.objects.filter(active=True).first()
    if active:
        user.institute = active
        user.save(update_fields=['institute'])
        return active

    return None


@login_required
def onboarding_step1(request):
    """Step 1: Institute profile — name, country, logo, motto."""
    institute = _resolve_institute(request.user)

    if request.method == 'POST':
        form = OnboardingStep1Form(
            request.POST, request.FILES,
            instance=institute,
        )
        if form.is_valid():
            inst = form.save(commit=False)
            inst.active = True
            if not inst.created_by_id:
                inst.created_by = request.user
            inst.save()
            request.user.institute = inst
            request.user.save(update_fields=['institute'])
            return redirect('institute:onboarding_step2')
    else:
        form = OnboardingStep1Form(instance=institute)

    ctx = {
        'form': form,
        **_onboarding_context(1),
    }
    return render(request, 'institute/onboarding/step1.html', ctx)


@login_required
def onboarding_step2(request):
    """Step 2: Departments + Academic Session."""
    institute = _resolve_institute(request.user)
    if not institute:
        return redirect('institute:onboarding_step1')

    # Pick up departments belonging to this institute,
    # plus any legacy departments that have no institute set yet.
    existing_departments = Department.objects.filter(
        models.Q(institute=institute) | models.Q(institute__isnull=True)
    )

    # Claim unlinked departments for this institute
    unlinked = existing_departments.filter(institute__isnull=True)
    if unlinked.exists():
        unlinked.update(institute=institute)

    existing_session = AcademicSession.objects.order_by('-year').first()

    existing_departments = Department.objects.filter(institute=institute)

    if request.method == 'POST':
        dept_formset = OnboardingDepartmentFormSet(
            request.POST, prefix='departments',
        )
        session_form = OnboardingAcademicSessionForm(
            request.POST, instance=existing_session,
        )
        if dept_formset.is_valid() and session_form.is_valid():
            existing_names = set(
                existing_departments.values_list('name', flat=True)
            )
            for dept_form in dept_formset:
                name = dept_form.cleaned_data.get('name', '').strip()
                if not name or name in existing_names:
                    continue
                Department.objects.create(
                    name=name,
                    short_name=dept_form.cleaned_data.get('short_name', ''),
                    code=dept_form.cleaned_data.get('code') or 0,
                    institute=institute,
                    created_by=request.user,
                )
                existing_names.add(name)
            session = session_form.save(commit=False)
            if not session.created_by_id:
                session.created_by = request.user
            session.save()
            return redirect('institute:onboarding_step3')
    else:
        dept_formset = OnboardingDepartmentFormSet(prefix='departments')
        session_form = OnboardingAcademicSessionForm(instance=existing_session)

    ctx = {
        'dept_formset': dept_formset,
        'session_form': session_form,
        'existing_departments': existing_departments,
        **_onboarding_context(2),
    }
    return render(request, 'institute/onboarding/step2.html', ctx)


@login_required
def onboarding_step3(request):
    """Step 3: Review and launch."""
    institute = _resolve_institute(request.user)
    if not institute:
        return redirect('institute:onboarding_step1')

    departments = Department.objects.filter(institute=institute)
    session = AcademicSession.objects.order_by('-year').first()

    if request.method == 'POST':
        institute.onboarding_completed = True
        institute.save(update_fields=['onboarding_completed'])
        request.session.pop('skip_onboarding', None)
        return redirect('index_view')

    ctx = {
        'institute': institute,
        'departments': departments,
        'session': session,
        **_onboarding_context(3),
    }
    return render(request, 'institute/onboarding/step3.html', ctx)
