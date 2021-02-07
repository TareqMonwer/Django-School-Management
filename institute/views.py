from django.core import serializers
from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView
from .models import InstituteProfile


class InstituteProfileConfigDashboard(UpdateView):
    model = InstituteProfile
    fields = '__all__'
    pk_url_kwarg = 'institute_pk'
    template_name = 'institute/dashboard/config_form.html'


class InstituteProfileDetailDashboard(DetailView):
    model = InstituteProfile
    pk_url_kwarg = 'institute_pk'
    template_name = 'institute/dashboard/config.html'

    def get_context_data(self, *args, **kwargs):
        ctx =  super().get_context_data(*args, **kwargs)
        institute_fields = serializers.serialize("python", InstituteProfile.objects.all())
        ctx['institute_fields'] = institute_fields
        return ctx