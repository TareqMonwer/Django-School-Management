from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.shortcuts import render
from django.urls import reverse_lazy
from articles.models import Article, Category
from articles.forms import ArticleForm
from articles.filters import ArticleFilter
from permission_handlers.administrative import user_is_admin_su_editor_or_ac_officer


class DashboardArticlePublishView(UserPassesTestMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'articles/dashboard/publish.html'

    def get(self, request, *args, **kwargs):
        """
        Ask publisher if they want to publish it on site only
        or they'd like to publish it in their other websites.
        """
        self.object = None
        ctx = super().get_context_data(*args, **kwargs)
        return render(
            request,
            'articles/dashboard/article_publisher_cta.html', ctx
        )
    
    def test_func(self):
        user = self.request.user
        return user_is_admin_su_editor_or_ac_officer(user)

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('account:profile_complete')
        return redirect('account_login')

dashboard_article_publish = DashboardArticlePublishView.as_view()


class DashboardManageArticleView(UserPassesTestMixin, ListView):
    queryset = Article.objects.filter(status='published')
    template_name = 'articles/dashboard/manage.html'

    def test_func(self):
        user =  self.request.user
        return user_is_admin_su_editor_or_ac_officer(user)
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['filter'] = ArticleFilter(
            self.request.GET,
            queryset=Article.objects.all()
        )
        return ctx

dashboard_manage_article = DashboardManageArticleView.as_view()


class DashboardArticleDeleteView(UserPassesTestMixin, DeleteView):
    model = Article
    success_url = reverse_lazy('articles:dashboard_manage')

    def test_func(self):
        user =  self.request.user
        return user_is_admin_su_editor_or_ac_officer(user)

dashboard_article_delete = DashboardArticleDeleteView.as_view()


def dashboard_article_draft(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if request.method == 'POST':
        article.status = 'draf'
        article.save()
        return redirect('articles:dashboard_manage')
