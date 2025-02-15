from django.contrib import admin

from payments.models import PaymentRecord

@admin.register(PaymentRecord)
class PaymentRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'payment_id', 'amount', 'status', 'created_at')
    search_fields = ('user__username', 'payment_id')
    list_filter = ('status', 'created_at')
    ordering = ('-created_at',)