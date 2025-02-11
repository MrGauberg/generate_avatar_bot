from django.contrib import admin
from .models import Package, Order

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'package_type', 'total_generations', 'used_generations', 'purchase_date')
    search_fields = ('user__username', 'package_type')
    list_filter = ('package_type', 'purchase_date')
    ordering = ('-purchase_date',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'package', 'order_id', 'status', 'created_at')
    search_fields = ('user__username', 'order_id')
    list_filter = ('status', 'created_at')
    ordering = ('-created_at',)
