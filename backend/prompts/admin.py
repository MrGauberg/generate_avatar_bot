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
    filter_horizontal = ('genders',)
    list_filter = ('category',)
    ordering = ('id',)
    list_editable = ('genders',)
