from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse, reverse_lazy


class Avatar(models.Model):
    name = models.CharField(max_length=32)
    image = models.ImageField(upload_to='avatars')

    def __str__(self):
        return f"{self.name}"

    def add_avatar_registration(value):
        user = User.objects.last()
        user.avatar = Avatar.objects.get(id=value)
        return user.save()

    @staticmethod
    def change_avatar(value, user):
        user = User.objects.get(id=user.id)
        user.avatar = Avatar.objects.get(id=value)
        return user.save()


class User(AbstractUser):
    avatar = models.ForeignKey(to=Avatar, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} ({self.username}) {self.last_name}"

    def get_absolute_url(self):
        return reverse("users:profile", kwargs={'pk': self.pk})