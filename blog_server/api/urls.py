from django.urls import path, include
from .views import ArticleApi, CommentApi, UsersApi
from rest_framework.routers import SimpleRouter, DefaultRouter

app_name = 'api'

router = DefaultRouter()
router.register('articles', ArticleApi)
router.register('Comments', CommentApi)
router.register('users', UsersApi)


urlpatterns = router.urls