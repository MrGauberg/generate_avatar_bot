from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'telegram_id', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'telegram_id')
    ordering = ('id',)
