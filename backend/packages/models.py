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
    name = models.CharField(max_length=40, default='Базовый')
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


class Payment(models.Model):
    """Модель платежей ЮKassa"""
    STATUS_CHOICES = (
        ('pending', 'Ожидание'),
        ('succeeded', 'Успешно'),
        ('canceled', 'Отменен'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments')
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='payments')
    payment_id = models.CharField(max_length=100, unique=True, help_text="ID платежа в ЮKassa")
    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Сумма платежа")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Платеж {self.payment_id} - {self.status}"
    
    class Meta:
        verbose_name = 'Платеж Юкасса'
        verbose_name_plural = 'Платежи Юкасса'
