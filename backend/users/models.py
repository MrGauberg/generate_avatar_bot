# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

from users.user_manager import CustomUserManager

class CustomUser(AbstractUser):
    telegram_id = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(unique=True)
    is_authorized = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class UserSettings(models.Model):
    PHOTO_FORMATS = [
        ('1:1', '1:1'),
        ('3:4', '3:4'),
        ('9:16', '9:16'),
        ('16:9', '16:9'),
    ]
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, related_name='settings')
    photo_format = models.CharField(max_length=10, choices=PHOTO_FORMATS, default='1:1')
    avatars_amount_available = models.IntegerField(default=1)


    def __str__(self):
        return self.user.email
    
    class Meta:
        verbose_name = 'Настройки пользователя'
        verbose_name_plural = 'Настройки пользователей'