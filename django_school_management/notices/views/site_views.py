from django.views.generic import FormView, ListView, DetailView
from notices.models import Notice, NoticeResponse


class NoticesPageView(ListView):
    model = Notice
    template_name = 'notices/site/list.html'
    context_object_name = 'notices'


class NoticeDetailView(DetailView):
    model = Notice
    template_name = 'notices/site/detail.html'
    context_object_name = 'notice'

    def get_context_data(self, *args, **kwargs):
        user = self.request.user
        context = super().get_context_data(*args, **kwargs)
        if user.is_authenticated:
            NoticeResponse.objects.get_or_create(
                notice=context.get('object'),
                responder=user
            )
            context['user_response_status'] = 'r'  # recorded
        else:
            context['user_response_status'] = 'nr'  # not recorded
        return context