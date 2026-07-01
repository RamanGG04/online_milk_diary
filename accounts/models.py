from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        OPERATOR = 'operator', 'Collection Operator'
        ACCOUNTANT = 'accountant', 'Accountant'
        FARMER = 'farmer', 'Farmer'

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.FARMER)
    phone = models.CharField(max_length=15, blank=True)

    def is_admin(self):
        return self.role == self.Role.ADMIN or self.is_superuser

    def is_operator(self):
        return self.role in (self.Role.OPERATOR, self.Role.ADMIN) or self.is_superuser

    def is_accountant(self):
        return self.role in (self.Role.ACCOUNTANT, self.Role.ADMIN) or self.is_superuser

    def is_farmer_user(self):
        return self.role == self.Role.FARMER
