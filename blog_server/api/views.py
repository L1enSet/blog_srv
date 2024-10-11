from django.http import JsonResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response

from blog.models import Article, Comment, ArticleLike
from users.models import User
from .serializers import ArticleSerializer, CommentSerializer, ArticleLikeSerializer, UserSerializer


class ArticleApi(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAdminUser]

    @action(detail=True, methods=['get'], name='comments_list')
    def comments(self, request, pk=None):
        obj = self.get_object()
        queryset = Comment.objects.filter(article=obj.id, is_deleted=False)
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], name='article_likes')
    def likes(self, request, pk=None):
        obj = self.get_object()
        queryset = ArticleLike.objects.filter(article=obj.id)
        serializer = ArticleLikeSerializer(queryset, many=True)

        return Response(serializer.data)


class CommentApi(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAdminUser]


class UsersApi(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    @action(detail=True, methods=['get'], name='user_comments')
    def my_comments(self, request, pk=None):
        obj = self.get_object()
        queryset = Comment.objects.filter(author=obj.id)
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)
