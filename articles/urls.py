from django.urls import path

from . import views

app_name = 'articles'

urlpatterns = [
    path('',
        views.ArticleList.as_view(),
        name='home'
    ),
    path('new/',
        views.ArticleCreate.as_view(),
        name='create'
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
]
