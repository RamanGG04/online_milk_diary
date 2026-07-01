from django.contrib import admin

from .models import MilkEntry, RateChart


@admin.register(RateChart)
class RateChartAdmin(admin.ModelAdmin):
    list_display = ['name', 'min_fat', 'max_fat', 'price_per_liter', 'is_active']


@admin.register(MilkEntry)
class MilkEntryAdmin(admin.ModelAdmin):
    list_display = ['farmer', 'date', 'shift', 'quantity_liters', 'fat_percent', 'total_amount']
    list_filter = ['date', 'shift']
    search_fields = ['farmer__name', 'farmer__farmer_id']
