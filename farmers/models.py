from django.conf import settings
from django.db import models


class CollectionCenter(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Farmer(models.Model):
    farmer_id = models.CharField(max_length=20, unique=True, verbose_name='Farmer ID')
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='farmer_profile',
    )
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    village = models.CharField(max_length=100)
    address = models.TextField(blank=True)
    bank_account = models.CharField(max_length=30, blank=True)
    ifsc_code = models.CharField(max_length=15, blank=True)
    center = models.ForeignKey(
        CollectionCenter,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='farmers',
    )
    animal_count = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.farmer_id} - {self.name}'
