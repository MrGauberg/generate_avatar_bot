from django.db import models
from django.conf import settings


class PaymentRecord(models.Model):
    """Модель платежей ЮKassa"""
    STATUS_CHOICES = (
        ('pending', 'Ожидание'),
        ('succeeded', 'Успешно'),
        ('canceled', 'Отменен'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments')
    payment_id = models.CharField(max_length=100, unique=True, help_text="ID платежа в ЮKassa")
    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Сумма платежа")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(default=dict)

    def __str__(self):
        return f"Платеж {self.payment_id} - {self.status}"
    
    class Meta:
        verbose_name = 'Платеж Юкасса'
        verbose_name_plural = 'Платежи Юкасса'
