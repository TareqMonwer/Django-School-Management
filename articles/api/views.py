from rest_framework import viewsets
from .serializers import ArticleSerializer
from articles.models import Article


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
