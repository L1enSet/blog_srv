from django import forms
from django.contrib.auth.forms import (AuthenticationForm, UserCreationForm, UserChangeForm, PasswordResetForm,
                                       SetPasswordForm)
from .models import User, Avatar
import re


class UserLogin(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': "line-form", 'placeholder': 'Enter a username'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': "line-form", 'placeholder': 'Enter a password'}))

    class Meta:
        model = User
        fields = ('username', 'password')

class UserRegistration(UserCreationForm):

    avatar = forms.ModelChoiceField(
        queryset=Avatar.objects.all(),
        required=False,
        widget=forms.RadioSelect(attrs={'class': "form-radio", 'multiple': 'true', 'aria-label': 'select tags'}))
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': "line-form", 'placeholder': 'Enter a firstname'}))
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': "line-form", 'placeholder': 'Enter a lastname'}))
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': "line-form", 'placeholder': 'Enter a username'}))
    email = forms.CharField(
        widget=forms.EmailInput(attrs={'class': "line-form", 'placeholder': 'Enter a email address'}))
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': "line-form", 'placeholder': 'Enter a password'}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': "line-form", 'placeholder': 'Repeat a password'}))

    class Meta:
        model = User
        fields = ('avatar', 'username', 'first_name', 'last_name', 'email', 'password1', 'password2')


    def valid_password(self):
        pattern_password = re.compile(r'^(?=.*[0-9].*)(?=.*[a-z].*)(?=.*[A-Z].*)[0-9a-zA-Z]{8,}$')
        return bool(pattern_password.match(self.password1))


class ChangeUser(UserChangeForm):
    avatar = forms.ModelChoiceField(
        queryset=Avatar.objects.all(),
        required=False,
        widget=forms.RadioSelect(attrs={'class': "form-radio", 'multiple': 'true', 'aria-label': 'select tags'}))
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': "line-form", 'placeholder': 'Enter a firstname'}))
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': "line-form", 'placeholder': 'Enter a lastname'}))
    email = forms.CharField(
        widget=forms.EmailInput(attrs={'class': "line-form", 'placeholder': 'Enter a email address'}))

    class Meta:
        model = User
        fields = ('avatar', 'first_name', 'last_name', 'email')
    
    def get_avatar(avatar_id):
        return Avatar.objects.get(id=id)


class UserForgotPasswordForm(PasswordResetForm):
    """
    сброс пароля
    """

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })


class UserSetNewPasswordForm(SetPasswordForm):
    """
    смена пароля
    """

    def __init__(self, *args, **kwargs):
        """
        обновить стили формы
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })