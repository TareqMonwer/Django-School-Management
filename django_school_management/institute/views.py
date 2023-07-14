from django.core import serializers
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView

from django_school_management.institute.forms.institute_profile_form import InstituteProfileCreateForm
from .models import InstituteProfile


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
            return render(request, 'permission_denied.html')
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
        ctx =  super().get_context_data(*args, **kwargs)
        institute_fields = serializers.serialize("python", InstituteProfile.objects.all())
        ctx['institute_fields'] = institute_fields
        return ctx


class SetActiveInstituteProfile(View):
    def get(self, request, institute_pk, *args, **kwargs):
        institute = InstituteProfile.objects.get(pk=institute_pk)
        institute.active = True
        institute.save()
        return redirect('institute:institute_detail', institute_pk)
