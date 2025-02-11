from django.contrib import admin
from .models import PromptCategory, PromptStyle

@admin.register(PromptCategory)
class PromptCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('id',)

@admin.register(PromptStyle)
class PromptStyleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category')
    search_fields = ('name', 'category__name')
    list_filter = ('category',)
    ordering = ('id',)
