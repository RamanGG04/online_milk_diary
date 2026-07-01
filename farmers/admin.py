from django.contrib import admin

from .models import CollectionCenter, Farmer


@admin.register(CollectionCenter)
class CollectionCenterAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'is_active']


@admin.register(Farmer)
class FarmerAdmin(admin.ModelAdmin):
    list_display = ['farmer_id', 'name', 'phone', 'village', 'center', 'is_active']
    list_filter = ['center', 'is_active', 'village']
    search_fields = ['farmer_id', 'name', 'phone']
