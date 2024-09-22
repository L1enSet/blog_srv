from django.urls import path
from .views import add_like, add_comment, add_like_comment, delete_comment, add_block

app_name = 'ajax'

urlpatterns = [
    path('art_contentblock/<int:article>', add_block, name='content_block'),
    path('art_likes/<int:article>', add_like, name='likes'),
    path('art_comment/<int:article>', add_comment, name='comment'),
    path('comment_like/<int:comment>', add_like_comment, name='like_comment'),
    path('delete_comment/<int:comment>', delete_comment, name='delete_comment')
]