import django_filters
from articles.models import Article


class ArticleFilter(django_filters.FilterSet):
    class Meta:
        model = Article
        fields = (
            'status', 'is_featured',
            'force_highlighted', 'created',
            'categories'
        )