from django.views.generic import ListView
from notices.models import Notice


class NoticesPageView(ListView):
    model = Notice
    template_name = 'notices/site/list.html'
    context_object_name = 'notices'
