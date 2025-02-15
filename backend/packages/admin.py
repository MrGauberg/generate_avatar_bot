from django.contrib import admin
from .models import Package, PackageType


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'package_type', 'generations_remains', 'purchase_date')
    search_fields = ('user__username', 'package_type__name')
    list_filter = ('package_type', 'purchase_date')
    ordering = ('-purchase_date',)

@admin.register(PackageType)
class PackageTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'total_generations', 'amount')
    search_fields = ('name',)
    list_filter = ('total_generations',)
    ordering = ('-total_generations',)

