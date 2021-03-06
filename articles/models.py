from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField
from autoslug import AutoSlugField
from bs4 import BeautifulSoup
from markdown import markdown
from model_utils.models import TimeStampedModel
from ckeditor_uploader.fields import RichTextUploadingField

from random import choice

from django.conf import settings
from django.db import models
from django.urls import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()\
            .filter(status='published')


class Article(TimeStampedModel):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )
    title = models.CharField("Article Title", max_length=255)
    featured_image = models.ImageField(upload_to="featured_images")
    slug = AutoSlugField("Article Address", unique=True,
                         always_update=False, populate_from='title')
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.DO_NOTHING)
    content = RichTextUploadingField(config_name='default')
    is_featured = models.BooleanField(default=False)
    force_highlighted = models.BooleanField(default=False)
    categories = TreeManyToManyField('Category', blank=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')

    objects = models.Manager()   # Default manager.
    published = PublishedManager()   # Custom published manager.
    likes = models.ManyToManyField(
        'Like', related_name='article_liked', blank=True)

    class Meta:
        ordering = ['-created']
        get_latest_by = "created"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('articles:detail', kwargs={'slug': self.slug})

    def short_description(self):
        choices = [10, 15, 18]
        html = markdown(self.content)
        text = ''.join(BeautifulSoup(html).findAll(text=True))
        text = text.replace('\xa0', ' ').replace('\n', ' ').split(' ')
        return ' '.join(text[:choice(choices)])

    def get_related_articles(self):
        try:
            articles = self.categories.last().article_set.all()
        except:
            articles = []
        return articles


class Comment(TimeStampedModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='comments'
    )
    article = models.ForeignKey(Article, on_delete=models.CASCADE,
        related_name='comments'
    )
    content = models.TextField()
    approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='comments_approved'
    )

    def __str__(self):
        return self.content


class Like(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} liked this post'


class Category(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    display_on_menu = models.BooleanField(default=False)
    parent = TreeForeignKey(
        'self', on_delete=models.CASCADE,
        null=True, blank=True, related_name='children'
    )
    slug = AutoSlugField(
        "Category Link", unique=True,
        always_update=False, populate_from='name'
    )
    created = models.DateField(auto_now_add=True, blank=True, null=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            'articles:category_articles', kwargs={'slug': self.slug}
        )

    @classmethod
    def get_article_for_category(self):
        """ Returns one article for each category. """
        categories = Category.objects.all()
        articles = [
            category.article_set.order_by('-created').first()
            for category in categories if category.article_set.exists()
        ]
        return articles


class Newsletter(TimeStampedModel):
    email = models.EmailField()

    def __str__(self):
        return self.email