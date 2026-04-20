from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect


class InstituteRequiredMixin(LoginRequiredMixin):
    """Ensures the user is logged in and belongs to an institute.
    Redirects to onboarding if no institute is set."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not getattr(request.user, 'institute', None):
            return redirect('institute:onboarding_step1')
        return super().dispatch(request, *args, **kwargs)


class InstituteScopedQuerysetMixin:
    """Filters ListView/DetailView querysets to the user's institute.
    The model must have an `institute` ForeignKey field."""

    institute_field = 'institute'

    def get_queryset(self):
        qs = super().get_queryset()
        institute = getattr(self.request.user, 'institute', None)
        if institute:
            return qs.filter(**{self.institute_field: institute})
        return qs.none()


class InstituteAutoSetMixin:
    """Auto-sets `institute` and `created_by` on form_valid for
    CreateView/UpdateView. Works with models that have these fields."""

    def form_valid(self, form):
        obj = form.save(commit=False)
        if hasattr(obj, 'institute') and not obj.institute:
            obj.institute = self.request.user.institute
        if hasattr(obj, 'created_by') and not obj.created_by:
            obj.created_by = self.request.user
        obj.save()
        form.save_m2m()
        return redirect(self.get_success_url())


def get_user_institute(user):
    """Helper for function-based views."""
    return getattr(user, 'institute', None)


def get_active_institute():
    """Return the active institute for public/unauthenticated context (e.g. admission form)."""
    from django_school_management.institute.models import InstituteProfile
    return InstituteProfile.objects.filter(active=True).first()
