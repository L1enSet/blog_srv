import json
from django.http import JsonResponse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.db.utils import IntegrityError
from blog.models import Article, ArticleLike, Comment, CommentLike, ArticleItem, Code
from blog.forms import CommentForm, CreateArticleItem, EditArticleTitle, EditArticleImage, EditArticleTags
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
def add_article_title(request, article):
    form = EditArticleTitle()
    article_obj = Article.objects.get(slug=article)
    data = json.loads(request.body)
    status = None
    err = None

    try:
        if form.is_valid(data=data):
            article_obj.title = data['title']
            article_obj.save()
            status = 'succes'
        else:
            status = 'erros'
    except Exception as exc:
        status = '500'
        err = exc

    return JsonResponse({
        "status": status,
        "object": article_obj.title,
        "err": err,
        })


@login_required
def editIntro(request, article):
    article_obj = Article.objects.get(slug=article)
    data = json.loads(request.body)
    status = None
    err = None #тут остановился


@login_required
def add_article_image(request, article):
    form = EditArticleImage()
    article_obj = Article.objects.get(slug=article)
    file = request.FILES.get("file")
    
    if form.is_valid(file=file):
        #create fss object
        fss = FileSystemStorage()
        fss.path("post_images")
        filename = fss.save(name = file.name, content=file)
        url = fss.url(filename)
        
        #change article object
        article_obj.image = filename
        article_obj.save()
        status = 'succes'
    else:
        status = 'error'

    return JsonResponse({
        "status": status,
        "img": article_obj.image.url,
        })


@login_required
def add_block(request, article):
    """
    Method for additional new blocks with text or image in an article
    
    :param - request(JSON string), article primary key
    :return - Json response status response message
    add to DB new instanse content of article
    """
    article_obj = Article.objects.get(slug=article)
    item_obj = ArticleItem()
    text = request.POST['text']
    code = request.POST['source_code']
    image = request.FILES.get("file")
    status = None
    error = "no error"
    print(request.POST)
    
    #valid file
    try:
        fss = FileSystemStorage()
        filename = fss.save(name = image.name, content=image)
    except AttributeError:
        filename = None
    #print("filename is - ", filename)

    #valid form
    try:
        item_obj.article = article_obj
        item_obj.source_code = Code.objects.get(name="text")

        if text != None and text != "":
            item_obj.source_code = Code.objects.get(name=code)
            item_obj.text = text
        if filename != None:
            item_obj.image = filename
        item_obj.save()
        status = 'success'
    except Exception as exc:
        status = 'error'
        print(exc)
    
    #create response
    response = {
        "status": status,
        "error": error,
        "id": item_obj.id,
        }
    
    try:
        if item_obj.image.url:
            response['img'] = item_obj.image.url
        if item_obj.text:
            response['source_code'] = item_obj.source_code.name
            response['text'] = item_obj.text
    except ValueError as exc:
        if item_obj.text:
            response['text'] = item_obj.text

    try:
        return JsonResponse(response)
    except IntegrityError as exc:
        print(exc)


@login_required
def edit_block(request, article):
    """
    Method for edit content blocks with text or image in an article
    
    :param - request(JSON string), article primary key
    :return - Json response status response message
    add to DB new instanse content of article
    """

    article_obj = Article.objects.get(slug=article)
    item_obj = ArticleItem.objects.get(id=request.POST['item'])
    text = request.POST['text']
    image = request.FILES.get("file")
    code = request.POST['code']
    status = None
    error = None
    print(request.POST)
    
    #valid file
    try:
        fss = FileSystemStorage()
        fss.path("post_images")
        filename = fss.save(name = image.name, content=image)
        url = fss.url(filename)
    except AttributeError:
        filename = None

    #valid form
    try:
        if text != None and text != "":
            item_obj.text = text
        if filename != None:
            item_obj.image = filename
        if code != None:
            item_obj.source_code = Code.objects.get(name=code)
        item_obj.save()
        status = 'success'
    except Exception as exc:
        status = 'error'
        error = exc

    return JsonResponse({
        "status": status,
        "error": error,
        "img": item_obj.image.url if item_obj.image else None,
        "text": item_obj.text,
        })


@login_required
def delete_article_item(request, item):
    data = {}
    try:
        obj_item = ArticleItem.objects.filter(id=item)
        obj_item.delete()
        data['status'] = 'success'
    except Exception as exc:
        data['status'] = 'error'
        data['error'] = exc
    
    return JsonResponse(data)


@login_required
def edit_article_tags(request, article):
    
    article_object = Article.objects.get(slug=article)
    tags = list(request.POST['tags'].split(","))
    status = None
    try:
        article_object.tags.set(tags)
        article_object.save()
        status = "succes"
    except Exception as exc:
        status = "error"

    return JsonResponse({
        'status': status,
    })
        

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


