# prompts/models.py
from django.db import models

class PromptCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Категория промпта'
        verbose_name_plural = 'Категории промптов'

class PromptStyle(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(PromptCategory, on_delete=models.CASCADE, related_name='styles', null=True, blank=True)

    def __str__(self):
        return f'{self.name} ({self.category.name})' if self.category else self.name
    
    class Meta:
        verbose_name = 'Стиль промпта'
        verbose_name_plural = 'Стили промптов'
