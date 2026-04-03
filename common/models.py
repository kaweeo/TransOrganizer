from django.db import models


class FuelType(models.TextChoices):
    GASOLINE = "gasoline", "Gasoline"
    DIESEL = "diesel", "Diesel"
    LPG = "lpg", "LPG"


class TimeStampedModel(models.Model):
    """
    Abstract base model that provides self-updating
    'created_at' and 'updated_at' fields.
    """
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        abstract = True


class FuelPriceSnapshot(TimeStampedModel):
    country = models.CharField(
        max_length=100,
    )

    currency = models.CharField(
        max_length=20,
    )

    fuel_type = models.CharField(
        max_length=20,
        choices=FuelType.choices,
    )

    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
    )

    source = models.CharField(
        max_length=50,
        default="collectapi",
    )

    is_current = models.BooleanField(
        default=True,
    )

    raw_payload = models.JSONField(
        default=dict,
        blank=True,
    )


    class Meta:
        indexes = [
            models.Index(
                fields=["country", "fuel_type", "is_current"]
            ),
            models.Index(
                fields=["created_at"]
            ),
        ]

    def __str__(self):
        return f"{self.country} {self.fuel_type} {self.price} {self.currency}"
