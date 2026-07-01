from django.contrib import admin

from .models import Deduction, Payment


@admin.register(Deduction)
class DeductionAdmin(admin.ModelAdmin):
    list_display = ['farmer', 'deduction_type', 'amount', 'month']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['farmer', 'month', 'net_amount', 'paid_amount', 'status']
    list_filter = ['status', 'month']
