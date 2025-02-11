# leonardo_service/models.py
from django.db import models
from django.conf import settings

class LeonardoGeneration(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    avatar_id = models.CharField(max_length=100)
    prompt = models.TextField()
    style = models.CharField(max_length=100, blank=True, null=True)
    generation_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, default='pending')  # pending, processing, completed
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Generation {self.generation_id} ({self.status}) for {self.user.username}"
