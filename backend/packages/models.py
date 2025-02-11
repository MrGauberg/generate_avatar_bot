# packages/models.py
from django.db import models
from django.conf import settings

class Package(models.Model):
    PACKAGE_TYPES = (
        ('basic', 'Базовый'),
        ('premium', 'Премиум'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='packages')
    package_type = models.CharField(max_length=20, choices=PACKAGE_TYPES)
    total_generations = models.IntegerField()
    used_generations = models.IntegerField(default=0)
    purchase_date = models.DateTimeField(auto_now_add=True)

    def remaining_generations(self):
        return self.total_generations - self.used_generations

    def __str__(self):
        return f'{self.package_type} пакет для {self.user.username}'

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order {self.order_id} - {self.status}'
