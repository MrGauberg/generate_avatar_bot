from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserSettings

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'telegram_id', 'is_staff', 'is_active', 'is_authorized')
    search_fields = ('username', 'email', 'telegram_id')
    ordering = ('id',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'telegram_id', 'is_authorized')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )


@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_email', 'photo_format', 'avatars_amount_available')
    search_fields = ('user__username', 'photo_format')
    list_editable = ('photo_format', 'avatars_amount_available')

    def get_email(self, obj):
        return obj.user.email

    get_email.short_description = 'Email'
