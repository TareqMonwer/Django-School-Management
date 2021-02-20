from rest_framework import serializers
from articles.models import Article


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['title', 'featured_image', 'author', 'content',
            'is_featured', 'force_highlighted', 'categories',
            'status'
        ]