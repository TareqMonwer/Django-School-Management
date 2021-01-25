from braces.views import LoginRequiredMixin

from django.http import Http404
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.views.generic import (
    ListView, DetailView,
    CreateView, UpdateView
)

from .models import Article, Like
from .mixins import AuthorArticleEditMixin
from .forms import ArticleForm
from permission_handlers.administrative import user_is_teacher_or_administrative



class ArticleList(ListView):
    """
    Returns a list of published articles.
    """
    model = Article
    paginate_by = 10
    template_name = 'articles/articles.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            last_article = Article.published.latest()
        except Article.DoesNotExist:
            last_article = None
        context['last_article'] = last_article
        return context

    def get_queryset(self):
        qs = Article.published.select_related('author').select_related().all()
        return qs


class ArticleDetail(DetailView):
    model = Article
    template_name = 'articles/detail.html'

    def get_object(self, qs=None):
        obj = super().get_object(queryset=qs)
        # If user is not the author of article
        if obj.status == 'draft' and obj.author != self.request.user:
            raise Http404()
        return obj

    def get_context_data(self, **kwargs):
        obj = super().get_object()
        context = super().get_context_data(**kwargs)
        likes = Like.objects.filter(article=obj)
        context['likes'] = likes
        return context


class ArticleCreate(
    AuthorArticleEditMixin, LoginRequiredMixin,
    UserPassesTestMixin, CreateView):
    # fields none need to set None to provide form_class
    # because it has some value in AuthorArticleEditMixin.
    fields = None
    form_class = ArticleForm

    def test_func(self):
        user =  self.request.user
        return user_is_teacher_or_administrative(user)

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('account:profile_complete')
        return redirect('account_login')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ArticleUpdate(AuthorArticleEditMixin, UpdateView):
    fields = None
    form_class = ArticleForm


class ArticleLike(LoginRequiredMixin, View):
    def post(self, request, slug):
        user = request.user
        article = Article.objects.get(slug=slug)
        Like.objects.create(user=user, article=article)
        return redirect(article.get_absolute_url())
