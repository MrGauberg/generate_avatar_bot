# packages/models.py

from django.db import models
from django.conf import settings


class PackageType(models.Model):
    name = models.CharField(max_length=40)
    total_generations = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Тип пакета'
        verbose_name_plural = 'Типы пакетов'

class Package(models.Model):
    PACKAGE_TYPES = (
        ('basic', 'Базовый'),
        ('premium', 'Премиум'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='packages')
    package_type = models.ForeignKey(PackageType, on_delete=models.CASCADE)
    generations_remains = models.IntegerField(default=0)
    purchase_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)

    def remaining_generations(self):
        return self.total_generations - self.used_generations

    def __str__(self):
        return f'{self.package_type} пакет для {self.user.username}'
    
    class Meta:
        verbose_name = 'Пакет'
        verbose_name_plural = 'Пакеты'
