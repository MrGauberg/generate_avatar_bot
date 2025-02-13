from django.contrib import admin
from .models import Package, PackageType, Payment

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'package_type', 'generations_remains', 'purchase_date')
    search_fields = ('user__username', 'package_type__name')
    list_filter = ('package_type', 'purchase_date')
    ordering = ('-purchase_date',)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'package', 'payment_id', 'amount', 'status', 'created_at')
    search_fields = ('user__username', 'payment_id')
    list_filter = ('status', 'created_at')
    ordering = ('-created_at',)

@admin.register(PackageType)
class PackageTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'total_generations', 'amount')
    search_fields = ('name',)
    list_filter = ('total_generations',)
    ordering = ('-total_generations',)

