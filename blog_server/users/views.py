from typing import Any
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib import auth
from .models import User, Avatar
from blog.utils import DataMixin
from .forms import ChangeUser, UserForgotPasswordForm, UserSetNewPasswordForm, UserLogin, UserRegistration
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import DetailView, UpdateView, FormView, CreateView


class Profile(DataMixin, DetailView):
    model = User
    template_name = "users/profile.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(request=self.request)
        return context


class ProfileEdit(UpdateView, DataMixin):
    model = User
    form_class = ChangeUser
    template_name = 'users/profile_edit.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(request=self.request)
        context['avatars'] = Avatar.objects.all()
        context2 = DataMixin.get_context_data(self, request=self.request)
        self.success_url = User.objects.get(pk=self.kwargs['pk']).get_absolute_url()
        return context | context2


class UserLoginView(LoginView):
    form_class = UserLogin
    template_name = "users/login.html"

    def get_success_url(self):
        return reverse('index')


class UserRegistrationView(CreateView):
    template_name = "users/registration.html"
    form_class = UserRegistration
    success_url = "index/"

    def get_context_data(self, **kwargs):
        context = {}
        context['form'] = self.get_form()
        context['avatars'] = Avatar.objects.all()
        return context
    
    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('users:login'))


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


class UserForgotPasswordView(SuccessMessageMixin, PasswordResetView):
    
    form_class = UserForgotPasswordForm
    template_name = 'users/user_password_reset.html'
    success_url = reverse_lazy('index')
    success_message = 'Письмо с инструкцией по восстановлению пароля отправлена на ваш email'
    subject_template_name = 'users/email/password_subject_reset_mail.txt'
    email_template_name = 'users/email/password_reset_mail.html'

    def get_context_data(self, **kwargs):
        content = super().get_context_data(**kwargs)
        content['title'] = 'Запрос на восстановление пароля'
        return content


class UserPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    

    form_class = UserSetNewPasswordForm
    template_name = 'users/user_password_set_new.html'
    success_url = reverse_lazy('index')
    success_message = 'Пароль успешно изменен. Можете авторизоваться на сайте.'
               
    def get_context_data(self, **kwargs):
        content = super().get_context_data(**kwargs)
        content['title'] = 'Установить новый пароль'
        return content
