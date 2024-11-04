from django.views.generic import CreateView


class CreatedByMixin:
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.save()
        super().form_valid(form)