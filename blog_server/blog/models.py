from string import ascii_letters
from random import randint
from datetime import datetime

from django.db import models
from django.urls import reverse
from users.models import User
#from .utils import gen_slug

def gen_slug():
    slug = ""
    for i in range(0,20):
        abc = ascii_letters
        index = randint(0, len(abc)-1)
        slug += ascii_letters[index]
        
    return slug

class Tag(models.Model):
    name = models.CharField(max_length=32, primary_key=True)

    def __str__(self):
        return self.name

    @staticmethod
    def get_choices():
        tag_lst = []
        for i in Tag.objects.all():
            tag_lst.append((i.name, i.pk))
        return tag_lst


class Code(models.Model):
    name = models.CharField(max_length=128, primary_key=True)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=256, blank=True, default=None)
    intro = models.TextField(blank=True, default=None)
    image = models.ImageField(upload_to='post_images', default=None, blank=True)
    slug = models.SlugField(null=False, unique=True, default=gen_slug())
    date = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tag', default=None, blank=True, null=True, related_name='tags')
    comments_on = models.BooleanField(default=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id} : {self.title} : {self.date} : {self.comments_on}"
    
    def get_absolute_url(self):
        return reverse("blog:article", kwargs={"article_slug": self.slug})

    def get_likes(self, *args, **kwargs):
        likes = ArticleLike.objects.filter(article=self)
        return str(len(likes))

    def get_comments(self):
        comments = Comment.objects.filter(article=self, is_deleted=False)
        return str(len(comments))

    def get_views(self):
        views = View.objects.filter(article=self)
        return str(len(views))

    def add_tags(self, tags):
        print("is_tags")
        print(tags)
        for i in tags:
            tag = Tag.objects.get(name=i)
            print(tag.name)
            self.tags.add(tag)
    
    def date_update(self):
        try:
            self.date = datetime.now()
            return 0
        except Exception as exc:
            return exc

    
    def create_article(self):
        new = self.objects.create()
        return new


class ArticleItem(models.Model):
    article = models.ForeignKey(to=Article, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images', null=True, blank=True, default=None)
    source_code = models.ForeignKey(to=Code, on_delete=models.CASCADE, null=True)
    text = models.TextField(null=True, blank=True, default=None)


class View(models.Model):
    article = models.ForeignKey(to=Article, on_delete=models.CASCADE)
    username = models.CharField(max_length=128, default="not_auth")
    user_ip = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.article.id} - {self.username} ({self.user_ip})"


class ArticleLike(models.Model):
    article = models.ForeignKey(to=Article, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.article} - {self.user}"


class Comment(models.Model):
    parrent_comm = models.ForeignKey(to='self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    article = models.ForeignKey(to=Article, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id} - {self.text[0:100]} - {self.article.title}:{self.author.username}"

    def get_likes(self):
        likes = CommentLike.objects.filter(comment=self)
        return str(len(likes))

    def get_replies(self, comment_id):
        return self.objects.filter(parrent_comm=self.objects.get(id=self.id))

    def to_delete(self, user):
        if user == self.author:
            self.is_deleted = True
            self.save()


class CommentLike(models.Model):
    comment = models.ForeignKey(to=Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.comment} - {self.user}"





class MyLink(models.Model):
    name = models.CharField(max_length=64)
    link = models.CharField(max_length=256)
    logo = models.ImageField(upload_to='links_images')

    def __str__(self):
        return f"{self.name}"


class AboutMe(models.Model):
    about_me = models.TextField()

    def __str__(self):
        return "About_me_text"


class Technology(models.Model):
    name = models.CharField(max_length=64)
    link = models.CharField(max_length=256)
    logo = models.ImageField(upload_to='links_images')

    def __str__(self):
        return f"{self.name}"
