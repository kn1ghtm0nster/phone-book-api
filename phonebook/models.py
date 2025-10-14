from django.db import models

# Create your models here.


class Contact(models.Model):
    full_name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name


class PhoneNumber(models.Model):
    phone_number = models.CharField(max_length=50, unique=True)
    contact = models.ForeignKey(
        Contact, related_name='phone_numbers', on_delete=models.CASCADE)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.phone_number
