import json
from django.http import JsonResponse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from blog.models import Article, ArticleLike, Comment, CommentLike
from blog.forms import CommentForm, CreateArticleItem
from users.models import User


@login_required
def add_like(request, article):
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


@login_required
def add_like_comment(request, comment):
    if request.method == 'POST':
        comment_obj = Comment.objects.get(id=comment)
        like = CommentLike()
        like.user = auth.get_user(request=request)
        like.comment = comment_obj
        if not CommentLike.objects.filter(comment=Comment.objects.get(id=comment), user=auth.get_user(request=request)):
            like.save()
        else:
            like = CommentLike.objects.filter(comment=Comment.objects.get(id=comment), user=auth.get_user(request=request))
            like.delete()
        data = {'likes': comment_obj.get_likes()}
        return JsonResponse(data)
    else:
        return JsonResponse({'error': "uncorrect method"})


@login_required
def add_comment(request, article):
    form = CommentForm(data=json.loads(request.body))
    article_obj = Article.objects.get(id=article)
    status = None

    if form.is_valid():
        form.save(article_id=article, request=request)
        status = 'succes'
    else:
        status = form.erros

    return JsonResponse({"status": status})


@login_required
def add_block(request, article):
    """
    Method for additional new blocks with text or image in an article
    
    :param - request(JSON string), article primary key
    :return - Json response status response message
    add to DB new instanse content of article
    """

    form = CreateArticleItem(data=json.loads(request.body))
    article_obj = Article.objects.get(id=article)
    status = None

    if form.is_valid():
        form.save(article_id=article, request=request)
        status = 'succes'
    else:
        status = form.erros

    return JsonResponse({"status": status})


@login_required
def delete_comment(request, comment):
    status = "not deleted"
    if request.method == "POST":
        comm = Comment.objects.get(id=comment)
        user = User.objects.get(id=int(request.user.id))
        if user == comm.author or user.is_superuser:
            comm.is_deleted = True
            comm.save()
            status = "is deleted"

    return JsonResponse({"status": status})


