from django.db import models
from django.conf import settings

class LeonardoGeneration(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    avatar_id = models.CharField(max_length=100)
    model_id = models.CharField(max_length=100, default='5c232a9e-9061-4777-980a-ddc8e65647c6')
    prompt = models.TextField()
    width = models.IntegerField(default=512)
    height = models.IntegerField(default=512)
    guidance_scale = models.IntegerField(default=7)
    generation_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, default='pending')  # pending, processing, completed
    created_at = models.DateTimeField(auto_now_add=True)
    api_credit_cost = models.IntegerField(default=0)

    def __str__(self):
        return f"Generation {self.generation_id} ({self.status}) for {self.user.username}"
    
    class Meta:
        verbose_name = 'Генерация'
        verbose_name_plural = 'Генерации'
