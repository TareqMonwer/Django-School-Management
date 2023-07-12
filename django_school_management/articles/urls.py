from django.urls import path

from . import views
from .dashboard_views import dashboard_views

app_name = 'articles'

urlpatterns = [
    path('',
        views.ArticleList.as_view(),
        name='home'
    ),
    path('all/', 
        views.AllArticles.as_view(), 
        name='all_articles'
    ),
    path('manage/', dashboard_views.dashboard_manage_article,
        name='dashboard_manage'
    ),
    path('manage/subscribers/', 
        dashboard_views.SubscribersManageView.as_view(),
        name='subscribers'
    ),
    path('dashboard/delete/<int:pk>/', 
        dashboard_views.dashboard_article_delete, 
        name='dashboard_article_delete'
    ),
    path('dashboard/new/',
         dashboard_views.dashboard_article_publish,
        name='dashboard_article_publish'
    ),
    path('dashboard/draft/<int:pk>/', 
        dashboard_views.dashboard_article_draft,
        name='dashboard_article_draft'
    ),
    path('dashboard/publish/article/',
         views.ArticleCreateFromDashboard.as_view(),
        name='publish_article_from_dashboard'
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
