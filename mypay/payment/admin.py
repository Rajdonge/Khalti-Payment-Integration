from django.contrib import admin
from . models import Payment

# Register your models here.
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['purchase_order_id', 'amount', 'name', 'email', 'phone', 'status', 'created_at']

admin.site.register(Payment, PaymentAdmin)