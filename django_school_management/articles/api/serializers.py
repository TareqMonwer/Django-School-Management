from rest_framework import serializers
from django_school_management.articles.models import Article


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'featured_image', 'author', 'content',
            'is_featured', 'force_highlighted', 'categories',
            'status'
        ]