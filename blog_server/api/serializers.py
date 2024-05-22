from rest_framework import serializers
from blog.models import Article, Comment, ArticleLike
from users.models import User

class ArticleSerializer(serializers.ModelSerializer):

    likes = serializers.SerializerMethodField('get_likes')
    comments = serializers.SerializerMethodField('get_comments')

    class Meta:
        model = Article
        fields = ('id', 'slug', 'title', 'intro', 'text', 'date', 'tags', 'image',
                  'comments_on', 'is_published', 'likes', 'comments')
        depth = 1

    def get_likes(self, obj):
        return obj.get_likes()

    def get_comments(self, obj):
        return obj.get_comments()


class CommentSerializer(serializers.ModelSerializer):

    likes = serializers.SerializerMethodField('get_likes')
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = Comment
        fields = ('id', 'author', 'parrent_comm', 'article', 'date', 'text', 'is_deleted', 'likes')
        depth = 1

    def get_likes(self, obj):
        return obj.get_likes()

class ArticleLikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ArticleLike
        fields = ('id', 'article', 'user')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'avatar')


