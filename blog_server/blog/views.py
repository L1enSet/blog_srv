from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.db.utils import IntegrityError
from random import randint
from .forms import CreateArticle, CommentForm
from .utils import *


class ListArticles(DataMixin, ListView):   
    model = Article
    template_name = "blog_app/index.html"
    errors = False

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(request=self.request)
        context['articles'] = self.model.objects.filter(is_published=True).order_by("-id").cache(ops=['get'])
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


class ViewCreateArticle(LoginRequiredMixin, CreateView, TextMixin, DataMixin):
    template_name = "blog_app/create_article.html"
    form_class = CreateArticle

    def get_context_data(self, **kwargs):
        context = super().get_context_data(request=self.request)
        context2 = DataMixin.get_context_data(self, request=self.request)
        return context | context2

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)

    def form_valid(self, form):
        try:
            article = form.save(commit=False)
            article.slug = self.gen_slug(title=article.title)
            article.save()
            form.save_m2m()

        except IntegrityError:
            # когда слаг не уникален
            article.slug += f'{randint(0,1000)}'
            article.save()
            form.save_m2m()

        return HttpResponseRedirect(Article.objects.get(slug=article.slug).get_absolute_url())


class ViewEditArticle(LoginRequiredMixin, UpdateView):
    model = Article
    form_class = CreateArticle
    template_name = "blog_app/edit_post.html"
    slug_url_kwarg = 'article_slug'








    
