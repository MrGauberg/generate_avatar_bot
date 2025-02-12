# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

from users.user_manager import CustomUserManager

class CustomUser(AbstractUser):
    telegram_id = models.CharField(max_length=50, blank=True, null=True)
    
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
