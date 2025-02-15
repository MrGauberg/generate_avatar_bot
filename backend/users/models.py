# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

from users.user_manager import CustomUserManager

class CustomUser(AbstractUser):
    telegram_id = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(unique=True)
    is_authorized = models.BooleanField(default=False)
    avatars_amount_available = models.IntegerField(default=1)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
