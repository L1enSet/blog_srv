
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from blog.views import ListArticles
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ListArticles.as_view(), name='index'),
    path('blog/', include('blog.urls', namespace='blog')),
    path('users/', include('users.urls', namespace='users')),
    path('api/', include('api.urls', namespace='api')),
    path('ajax/', include('ajax.urls', namespace='ajax'))
]
if settings.DEBUG == True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)