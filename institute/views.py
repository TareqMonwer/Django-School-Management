from django.core import serializers
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView

from institute.forms.institute_profile_form import InstituteProfileCreateForm
from .models import InstituteProfile


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