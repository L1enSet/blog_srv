import json
from django import forms
from django.forms import modelformset_factory
from django.contrib import auth
from .models import Article, Comment, Tag, ArticleItem


class CreateArticle(forms.ModelForm):

    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control py-4", 'placeholder': 'Enter a title'}))
    intro = forms.CharField(
        widget=forms.Textarea(attrs={'class': "form-control mb-2", 'type': 'text'}))
    text = forms.CharField(
        widget=forms.Textarea(attrs={'class': "form-control mb-2", 'type': 'text', 'required': 'true'}))
    image = forms.ImageField(
        widget=forms.FileInput(attrs={'class': 'custom-file-input'}))
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        to_field_name='name',
        widget=forms.SelectMultiple(attrs={'class': "form-select", 'multiple': 'true', 'aria-label': 'select tags'}))
    сomments_on = forms.CheckboxInput()

    is_published = forms.CheckboxInput()

    class Meta:
        model = Article
        fields = ('title', 'intro', 'text', 'image', 'tags', 'comments_on', 'is_published')


class CreateArticleItem(forms.ModelForm):
    image = forms.ImageField(
        widget=forms.FileInput(attrs={'class': 'custom-file-input'}))
    
    text = forms.CharField(
        widget=forms.Textarea(attrs={'class': "form-control mb-2", 'type': 'text', 'required': 'true'}))
    
    class Meta:
        model = ArticleItem
        fields = ('image', 'text')


class EditArticle(forms.ModelForm):

    widgets = {'title': forms.TextInput(attrs={'class': "form-control py-4", 'placeholder': 'Enter a title'}),
               'intro': forms.Textarea(attrs={'class': "form-control mb-2", 'type': 'text'}),
               #'text': forms.Textarea(attrs={'class': "form-control mb-2", 'type': 'text'}),
               'image': forms.FileInput(attrs={'class': 'custom-file-input'}),
               'slug': forms.TextInput(attrs={'class': "form-control py-4", 'placeholder': 'Enter a slug'}),
               }

    class Meta:
        model = Article
        fields = ('title', 'intro', 'image', 'slug') #text


class CommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'class': "form-control mb-2 form-comment", 'type': 'text', 'rows': 3, 'placeholder': 'Напишите комментарий', 'required': 'true'}))
    parrent = forms.CharField(widget=forms.Textarea(attrs={'class': "form-control mb-2", 'type': 'text', 'required': 'false', 'hidden': 'true'}), required=False)

    class Meta:
        model = Comment
        fields = ('parrent', 'text')

    def save(self, request, article_id):
        comm = Comment()
        form = json.loads(request.body)

        if form['parrent']:
            comm.parrent_comm = Comment.objects.get(id=int(form['parrent']))

        comm.author = auth.get_user(request)
        comm.article = Article.objects.get(id=article_id)
        comm.text = form['text']
        comm.save()


class DeleteCommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = []