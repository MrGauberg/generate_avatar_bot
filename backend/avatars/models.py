from django.db import models
from django.conf import settings


class AvatarGender(models.Model):
    gender = models.CharField(max_length=40)

    def __str__(self):
        return f"Пол: {self.gender}"
    
    class Meta:
        verbose_name = 'Пол'
        verbose_name_plural = 'Пол'


class Avatar(models.Model):
    """Модель для хранения информации об аватаре пользователя"""
    GENDER_CHOICES = [
        ('male', 'Мужчина'),
        ('female', 'Женщина'),
        ('child', 'Ребенок'),
    ]

    name = models.CharField(max_length=100, default="Model")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="avatars")
    dataset_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    model_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    gender = models.ForeignKey(AvatarGender, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    api_credit_cost = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"Avatar ({self.gender}) for {self.user.username}"
    
    class Meta:
        verbose_name = 'Аватар'
        verbose_name_plural = 'Аватары'


class AvatarImage(models.Model):
    """Модель для хранения загруженных изображений аватара"""
    avatar = models.ForeignKey(Avatar, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="avatars/")

    def __str__(self):
        return f"Image for Avatar {self.avatar.id}"
    
    class Meta:
        verbose_name = 'Изображение аватара'
        verbose_name_plural = 'Изображения аватаров'


class AvatarSettings(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2, default=490.00)

    def __str__(self):
        return f"Стоимость аватара: {self.price}₽"
    
    class Meta:
        verbose_name = 'Настройки аватара'
        verbose_name_plural = 'Настройки аватаров'
    

class PhotoFormat(models.Model):
    format = models.CharField(max_length=10)

    def __str__(self):
        return f"Формат: {self.format}"
    
    class Meta:
        verbose_name = 'Формат фото'
        verbose_name_plural = 'Форматы фото'

