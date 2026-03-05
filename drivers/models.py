from django.db import models


class Driver(models.Model):
    name = models.CharField(
        max_length=100,
    )
    license_number = models.CharField(
        max_length=50,
        unique=True,
    )
    phone_number = models.CharField(
        max_length=20,
    )
    hired_date = models.DateField()

    def __str__(self):
        return f"{self.name} ({self.license_number})"
