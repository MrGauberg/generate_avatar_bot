from django.db import models
from django.conf import settings

class Avatar(models.Model):
    """Модель для хранения информации об аватаре пользователя"""
    GENDER_CHOICES = [
        ('male', 'Мужчина'),
        ('female', 'Женщина'),
        ('child', 'Ребенок'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="avatars")
    dataset_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    model_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Avatar ({self.gender}) for {self.user.username}"


class AvatarImage(models.Model):
    """Модель для хранения загруженных изображений аватара"""
    avatar = models.ForeignKey(Avatar, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="avatars/")

    def __str__(self):
        return f"Image for Avatar {self.avatar.id}"
