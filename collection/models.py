from decimal import Decimal

from django.conf import settings
from django.db import models

from farmers.models import Farmer


class RateChart(models.Model):
    name = models.CharField(max_length=50)
    min_fat = models.DecimalField(max_digits=4, decimal_places=2)
    max_fat = models.DecimalField(max_digits=4, decimal_places=2)
    price_per_liter = models.DecimalField(max_digits=8, decimal_places=2)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['min_fat']

    def __str__(self):
        return f'{self.name} ({self.min_fat}-{self.max_fat}%): Rs.{self.price_per_liter}/L'

    @classmethod
    def get_rate_for_fat(cls, fat_percent):
        fat = Decimal(str(fat_percent))
        rate = cls.objects.filter(
            is_active=True,
            min_fat__lte=fat,
            max_fat__gte=fat,
        ).first()
        if rate:
            return rate.price_per_liter
        default = cls.objects.filter(is_active=True).order_by('min_fat').first()
        return default.price_per_liter if default else Decimal('40.00')


class MilkEntry(models.Model):
    class Shift(models.TextChoices):
        MORNING = 'morning', 'Morning'
        EVENING = 'evening', 'Evening'

    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='milk_entries')
    date = models.DateField()
    shift = models.CharField(max_length=10, choices=Shift.choices)
    quantity_liters = models.DecimalField(max_digits=8, decimal_places=2)
    fat_percent = models.DecimalField(max_digits=4, decimal_places=2, default=Decimal('0'))
    snf_percent = models.DecimalField(max_digits=4, decimal_places=2, default=Decimal('0'))
    rate_per_liter = models.DecimalField(max_digits=8, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    entered_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']
        unique_together = ['farmer', 'date', 'shift']

    def __str__(self):
        return f'{self.farmer.name} - {self.date} ({self.get_shift_display()})'

    def save(self, *args, **kwargs):
        if not self.rate_per_liter:
            self.rate_per_liter = RateChart.get_rate_for_fat(self.fat_percent)
        self.total_amount = self.quantity_liters * self.rate_per_liter
        super().save(*args, **kwargs)
