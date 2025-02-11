# prompts/models.py
from django.db import models

class PromptCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class PromptStyle(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(PromptCategory, on_delete=models.CASCADE, related_name='styles')

    def __str__(self):
        return f'{self.name} ({self.category.name})'
