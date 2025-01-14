from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.db.utils import IntegrityError
from random import randint
from .forms import CreateArticle, CommentForm, CreateArticleItem, EditArticleTitle, EditArticleImage, EditArticleTags
from users.forms import UserLogin
from .models import Tag
from datetime import datetime
from .models import ArticleItem, Article, Code, gen_slug
from .utils import *


def create_article(request):
    response_url = 'index'
    if request.method == 'GET':
        if request.user.is_superuser:
            obj = Article.objects.create(title="", intro="")
            
            return HttpResponseRedirect(obj.get_absolute_url())
    else:
        return HttpResponseRedirect(reverse(response_url))
            

class ListArticles(DataMixin, ListView):   
    model = Article
    template_name = "blog_app/index.html"
    errors = False

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(request=self.request)
        context['articles'] = self.model.objects.filter(is_published=True).order_by("-id")
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)


class ListArticlesFilter(ListArticles):

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(request=self.request)
        context['articles'] = self.model.objects.filter(is_published=True, tags=Tag.objects.get(name=self.kwargs['tag_name'])).order_by("-id")
        if self.request.user.is_superuser:
            context['no_published_articles'] = self.model.objects.filter(is_published=False)
        return context


class ViewArticle(DataMixin, DetailView):
    model = Article
    template_name = "blog_app/detail_post.html"
    slug_url_kwarg = 'article_slug'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(request=self.request)
        context['article'] = self.get_object()
        context['article_items'] = ArticleItem.objects.filter(article=self.get_object())
        context['comment_form'] = CommentForm()
        context['comment'] = Comment.objects.filter(is_deleted=False, article=self.get_object())

        return context
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(**kwargs)
        if self.object:
            self.add_view_post(request, self.object.id)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(**kwargs)

        if context['comment_form']:
            self.add_comment(request=request)

        return self.render_to_response(context)
    
    def add_view_post(self, request, article_id):
        article = Article.objects.get(id=article_id)
        user = auth.get_user(request).username
        ip = request.META.get('REMOTE_ADDR', '')
        if not View.objects.filter(article=article, user_ip=ip):
            if not user:
                user = 'not_auth'
            view = View(article=article, username=user, user_ip=ip)
            view.save()


class ViewCreateArticle(LoginRequiredMixin, TemplateView, TextMixin, DataMixin):
    template_name = "blog_app/create_article.html"
    form_class = CreateArticle

    def get_context_data(self, **kwargs):
        context = super().get_context_data(request=self.request)
        context2 = DataMixin.get_context_data(self, request=self.request)
        return context | context2

    def get(self, request, *args, **kwargs):
        new_article = Article.create_article

    """def post(self, request, *args, **kwargs):
        print(request.POST)
        form = self.get_form()
        context = self.get_context_data(**kwargs)
        if context['form'].is_valid():
            self.form_valid(form = context['form'])
        return HttpResponseRedirect("index")"""

    """def form_valid(self, form):
        try:
            article = form.save(commit=False)
            article.slug = self.gen_slug(title=article.title)
            article.save()
            form.save_m2m()

        except IntegrityError:
            # когда слаг не уникален
            article = form.save(commit=False)
            article.slug += f'{randint(0,1000)}'
            article.save()
            form.save_m2m()

        return HttpResponseRedirect(Article.objects.get(slug=article.slug).get_absolute_url())"""


"""def ViewCreateArticleF(request):

    context = {
        'form': CreateArticle(),
        'content_forms': ArticleItemFormSet()
        }

    context['form_login'] = UserLogin()
    context['tag_list'] = Tag.objects.all()
    if request.user.is_superuser:
        context['no_published_articles'] = Article.objects.filter(is_published=False)

    if request.method == 'POST':
        if context['form'].is_valid():
            try:
                article = context['form'].save(commit=False)
                article.slug = TextMixin.gen_slug(title=article.title)
                article.save()
                context['form'].save_m2m()

                for i in context['content_forms']:
                    print(i.data)
                    if i.is_valid():
                        print("form is valid!")

            except IntegrityError:
                # когда слаг не уникален
                article = context['form'].save(commit=False)
                article.slug += f'{randint(0, 1000)}'
                article.save()
                context['form'].save_m2m()

            return HttpResponseRedirect(Article.objects.get(slug=article.slug).get_absolute_url())
        else:
            print(context['form'].data)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "blog_app/create_article.html", context)"""


class ViewEditArticle(PermissionRequiredMixin, LoginRequiredMixin, UpdateView, DataMixin):
    model = Article
    login_url = '/login/'
    permission_required = 'blog.chancge_article'
    form_class = CreateArticle
    template_name = "blog_app/edit_post.html"
    slug_url_kwarg = 'article_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(request=self.request)
        context['article'] = self.get_object()
        context['content_blocks'] = ArticleItem.objects.filter(article=self.get_object())
        context['form_title'] = EditArticleTitle(data={'title': self.get_object().title})
        context['form_image'] = EditArticleImage()
        context['form_tags'] = EditArticleTags()
        context['source_code'] = Code.objects.all()
        context2 = DataMixin.get_context_data(self, request=self.request)
        return context | context2

@login_required
def set_state(request, article, setting_type):
    user = auth.get_user(request)
    obj = Article.objects.get(slug=article)
    response = HttpResponseRedirect(obj.get_absolute_url())

    if user.is_superuser:
        if setting_type=='comment':
            if obj.comments_on==True:
                obj.comments_on = False
            else:
                obj.comments_on = True
        elif setting_type=='public':
            if obj.is_published == True:
                obj.is_published = False
            else:
                obj.is_published = True
                obj.date_update()
        obj.save()
    
    return response

    
        








    
