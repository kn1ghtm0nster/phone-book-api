from django.db import models
from typing import TYPE_CHECKING

# Create your models here.


class Contact(models.Model):
    full_name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    if TYPE_CHECKING:
        phone_number: 'PhoneNumber | None'

    def __str__(self):
        return self.full_name


class PhoneNumber(models.Model):
    phone_number = models.CharField(max_length=50, unique=True)
    contact = models.OneToOneField(
        Contact, related_name='phone_number', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.phone_number
