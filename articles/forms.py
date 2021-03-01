from mptt.forms import TreeNodeMultipleChoiceField
from django import forms
from .models import Article, Category, Comment


class ArticleForm(forms.ModelForm):
    category = TreeNodeMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=Category.objects.filter(children=None),
    )

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