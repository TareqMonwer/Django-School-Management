from .models import Article


class AuthorMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(author=self.request.user)


class AuthorEditMixin:
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class AuthorArticleMixin(AuthorMixin):
    model = Article


class AuthorArticleEditMixin(AuthorArticleMixin, AuthorEditMixin):
    fields = ['title', 'content']
