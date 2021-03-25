from django.views.generic import ListView, DetailView
from notices.models import Notice


class NoticesPageView(ListView):
    model = Notice
    template_name = 'notices/site/list.html'
    context_object_name = 'notices'


class NoticeDetailView(DetailView):
    model = Notice
    template_name = 'notices/site/detail.html'
    context_object_name = 'notice'
