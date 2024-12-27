from django.urls import path, include
from .views import ListArticles, ListArticlesFilter, ViewArticle, ViewCreateArticle, ViewEditArticle, set_state, create_article


app_name = 'blog_app'

urlpatterns = [
    path('tag/<str:tag_name>/', ListArticlesFilter.as_view(), name='article_filter'),
    path('article/<slug:article_slug>/', ViewArticle.as_view(), name='article'),
    path('create_article/', create_article, name='create_article'),
    path('edit_article/<slug:article_slug>/', ViewEditArticle.as_view(), name='edit_article'),
    path('article/add_like/<int:article>/', ViewArticle.add_like_aritcle, name='article_like'),
    path('comment<int:comment>add_like/', ViewArticle.add_like_comment, name='comment_like'),
    path('article/set_state/<str:article>/<str:setting_type>/', set_state, name='set_state'),
]

