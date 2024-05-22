from django.urls import path, include
from .views import logout, Profile, ProfileEdit, UserForgotPasswordView, UserPasswordResetConfirmView, UserLoginView, UserRegistrationView


app_name = 'users'

urlpatterns = [
    path('login/', 
         UserLoginView.as_view(), name='login'),
     
     path('registration/',
          UserRegistrationView.as_view(), name='registration'),

    path('profile/<int:pk>/',
         Profile.as_view(), name='profile'),

    path('profile_edit/<int:pk>/',
         ProfileEdit.as_view(), name='profile_edit'),

    path('logout/',
         logout, name='logout'),

    path('password-reset/',
         UserForgotPasswordView.as_view(), name='password_reset'),
    
    path('set-new-password/<uidb64>/<token>/',
         UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]