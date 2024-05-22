from .models import *
from users.forms import UserLogin, UserRegistration
from .models import Tag, ArticleLike, CommentLike, Comment
from django.http import JsonResponse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy, reverse


class DataMixin:
    
    def get_context_data(self, request):
        context = {}
        context['form_login'] = UserLogin()
        context['tag_list'] = Tag.objects.all()
        if self.request.user.is_superuser:
            context['no_published_articles'] = Article.objects.filter(is_published=False)
    
        return context
    
    def get_form(request):
        forms = {
            'login_form': UserLogin,
            'register_form': UserRegistration,
        }

    @login_required
    def add_like_aritcle(request, article):
        try:
            article_ins = Article.objects.get(id=article)
            like = ArticleLike()
            like.user = auth.get_user(request=request)
            like.article = article_ins
            if not ArticleLike.objects.filter(article=Article.objects.get(id=article), user=auth.get_user(request=request)):
                like.save()
            else:
                like = ArticleLike.objects.filter(article=Article.objects.get(id=article), user=auth.get_user(request=request))
                like.delete()
            data = {'likes': article_ins.get_likes()}
            return JsonResponse(data)
        except ValueError:
            return reverse_lazy("login")

    @login_required
    def add_like_comment(request, comment):
        like = CommentLike()
        like.user = auth.get_user(request=request)
        like.comment = Comment.objects.get(id=comment)
        like.save()
        return HttpResponseRedirect(reverse('index'))


class TextMixin:

    def gen_slug(self, title):
        return self.translit_rus(rus=title.lower())

    @staticmethod
    def translit_rus(rus):

        translit_table = {
            "а": "a",
            "б": "b",
            "в": "v",
            "г": "g",
            "д": "d",
            "е": "e",
            "ё": "e",
            "ж": "j",
            "з": "z",
            "ы": "i",
            "и": "i",
            "й": "i",
            "к": "k",
            "л": "l",
            "м": "m",
            "н": "n",
            "о": "o",
            "п": "p",
            "р": "r",
            "с": "s",
            "т": "t",
            "у": "u",
            "ф": "f",
            "х": "h",
            "ц": "c",
            "ч": "ch",
            "ш": "sh",
            "щ": "sh",
            "ь": "",
            "ъ": "",
            "э": "e",
            "ю": "yu",
            "я": "ya",
            " ": "_",
            ",": "",
            ".": "",
            "-": "_",
            "1": "1",
            "2": "2",
            "3": "3",
            "4": "4",
            "5": "5",
            "6": "6",
            "7": "7",
            "8": "8",
            "9": "9",
            "0": "0",
        }

        result = ""

        for i in tuple(rus):
            try:
                result += translit_table[i]
            except KeyError:
                result += i

        return result

    
    
