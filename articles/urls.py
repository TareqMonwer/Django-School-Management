from django.urls import path

from . import views
from .dashboard_views import dashboard_views

app_name = 'articles'

urlpatterns = [
    path('',
        views.ArticleList.as_view(),
        name='home'
    ),
    path('dashboard/new/',
         dashboard_views.dashboard_article_publish,
        name='dashboard_article_publish'
    ),
    path('new/',
        views.ArticleCreate.as_view(),
        name='create'
    ),
    path('newsletter/',
        views.newsletter,
        name='newsletter'
    ),
    path('author/<str:slug>/',
        views.AuthorProfile.as_view(),
        name='author_profile'
    ),
    path('<slug:slug>/update/',
        views.ArticleUpdate.as_view(),
        name='update'
    ),
    path('<slug:slug>/like/',
        views.ArticleLike.as_view(),
        name='like'
    ),
    path('<slug:slug>/',
        views.ArticleDetail.as_view(),
        name='detail'
    ),
    path('<slug:slug>/articles/',
        views.CategoryArticles.as_view(),
        name='category_articles'
    ),
]
