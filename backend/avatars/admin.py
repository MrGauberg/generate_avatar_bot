from django.contrib import admin
from .models import Avatar, AvatarImage

@admin.register(Avatar)
class AvatarAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'is_active', 'gender', 'created_at')
    search_fields = ('user__username', 'gender')
    list_editable = ('is_active',)
    list_filter = ('gender', 'created_at')

@admin.register(AvatarImage)
class AvatarImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'avatar', 'image')
    search_fields = ('avatar__user__username',)
    list_filter = ('avatar__gender',)

