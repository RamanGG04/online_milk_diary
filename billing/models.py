from django.db import models

from farmers.models import Farmer


class Deduction(models.Model):
    class DeductionType(models.TextChoices):
        FEED = 'feed', 'Feed Advance'
        LOAN = 'loan', 'Loan EMI'
        OTHER = 'other', 'Other'

    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='deductions')
    deduction_type = models.CharField(max_length=20, choices=DeductionType.choices)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.DateField(help_text='Use first day of the month')
    description = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-month', '-created_at']

    def __str__(self):
        return f'{self.farmer.name} - {self.get_deduction_type_display()} ({self.month})'


class Payment(models.Model):
    class PaymentMode(models.TextChoices):
        CASH = 'cash', 'Cash'
        BANK = 'bank', 'Bank Transfer'
        UPI = 'upi', 'UPI'

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        PAID = 'paid', 'Paid'

    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='payments')
    month = models.DateField(help_text='First day of billing month')
    total_liters = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    gross_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_deductions = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    net_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    payment_mode = models.CharField(max_length=20, choices=PaymentMode.choices, blank=True)
    paid_on = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-month', '-created_at']
        unique_together = ['farmer', 'month']

    def __str__(self):
        return f'{self.farmer.name} - {self.month.strftime("%B %Y")}'
