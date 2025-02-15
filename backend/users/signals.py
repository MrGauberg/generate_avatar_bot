import os
from django.db.models.signals import post_save    
from django.dispatch import receiver
from django.core.files.storage import default_storage
from .models import CustomUser, UserSettings

@receiver(post_save, sender=CustomUser)
def create_user_settings(sender, instance, **kwargs):
    """Создает настройки пользователя при его создании"""
    if not UserSettings.objects.filter(user=instance).exists():
        UserSettings.objects.get_or_create(user=instance)
    
