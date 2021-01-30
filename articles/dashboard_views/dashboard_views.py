from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import CreateView
from django.shortcuts import render
from articles.models import Article, Category
from articles.forms import ArticleForm
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
