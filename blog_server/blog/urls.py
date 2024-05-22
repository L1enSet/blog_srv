from django.urls import path, include
from .views import ListArticles, ListArticlesFilter, ViewArticle, ViewCreateArticle, ViewEditArticle


app_name = 'blog_app'

urlpatterns = [
    path('tag/<str:tag_name>/', ListArticlesFilter.as_view(), name='article_filter'),
    path('article/<slug:article_slug>/', ViewArticle.as_view(), name='article'),
    path('create_article/', ViewCreateArticle.as_view(), name='create_article'),
    path('edit_article/<slug:article_slug>/', ViewEditArticle.as_view(), name='edit_article'),
    path('article/add_like/<int:article>/', ViewArticle.add_like_aritcle, name='article_like'),
    path('comment<int:comment>add_like/', ViewArticle.add_like_comment, name='comment_like'),
]

