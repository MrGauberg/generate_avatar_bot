from django.contrib import admin

from .models import LeonardoGeneration


@admin.register(LeonardoGeneration)
class LeonardoGenerationAdmin(admin.ModelAdmin):
    list_display = ('generation_id', 'user', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('user__username', 'generation_id')
