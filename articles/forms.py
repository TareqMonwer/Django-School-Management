from tinymce.widgets import TinyMCE
from mptt.forms import TreeNodeMultipleChoiceField
from django import forms
# from django.contrib.flatpages.models import FlatPage
from .models import Article, Category, Comment


class ArticleForm(forms.ModelForm):
    category = TreeNodeMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=Category.objects.filter(children=None),
    )
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    class Meta:
        model = Article
        fields = ['title', 'content', 'featured_image',]


class ArticleUpdateForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'featured_image',]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', ]
