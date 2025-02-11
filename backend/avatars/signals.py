import os
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.core.files.storage import default_storage
from .models import AvatarImage

@receiver(post_delete, sender=AvatarImage)
def delete_avatar_image_file(sender, instance, **kwargs):
    """Удаляет файл изображения при удалении объекта AvatarImage"""
    if instance.image and default_storage.exists(instance.image.name):
        default_storage.delete(instance.image.name)
