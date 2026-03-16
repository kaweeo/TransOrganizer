from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from .validators import validate_plate_number, validate_fuel_consumption


class VehicleType(models.TextChoices):
    TANK = "tank", "Tank Truck"
    REFRIGERATED = "refrigerated", "Refrigerated Truck"
    REGULAR = "regular", "Regular Truck"
    EXPRESS = "express", "Express Van"


class Vehicle(models.Model):

    plate_number = models.CharField(
        max_length=15,
        unique=True,
        validators=[
            validate_plate_number,
        ],
    )

    brand = models.CharField(
        max_length=50
    )

    photo_url = models.URLField(
        blank=True,
        null=True,
        help_text="Link to a vehicle photo"
    )

    capacity = models.PositiveIntegerField(
        validators=[
            MinValueValidator(100),
        ],
        help_text="Capacity in kilograms"
    )

    fuel_consumption = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[
            validate_fuel_consumption,
        ],
        help_text="Liters per 100km"
    )

    vehicle_type = models.CharField(
        max_length=20,
        choices=VehicleType,
    )

    drivers = models.ManyToManyField(
        "drivers.Driver",
        related_name="vehicles",
        blank=True
    )

    class Meta:
        verbose_name = "Vehicle"
        verbose_name_plural = "Vehicles"

        indexes = [
            models.Index(
                fields=["plate_number"]
            ),
            models.Index(
                fields=["vehicle_type"]
            ),
        ]

    def clean(self):
        """
        Model-level validation.
        """
        if self.capacity < 500 and self.vehicle_type == VehicleType.TANK:
            raise ValidationError(
                "Tank trucks must have capacity at least 500 kg."
            )

    def __str__(self):
        return f"{self.plate_number} ({self.vehicle_type})"


class TankTruck(Vehicle):

    liquid_type = models.CharField(
        max_length=50,
        help_text="Type of liquid transported"
    )

    def save(self, *args, **kwargs):
        self.vehicle_type = VehicleType.TANK
        super().save(*args, **kwargs)


class RefrigeratedTruck(Vehicle):

    min_temperature = models.IntegerField(
        help_text="Minimum cooling temperature in Celsius"
    )

    def save(self, *args, **kwargs):
        self.vehicle_type = VehicleType.REFRIGERATED
        super().save(*args, **kwargs)


class RegularTruck(Vehicle):

    trailer_attached = models.BooleanField(
        default=False
    )

    def save(self, *args, **kwargs):
        self.vehicle_type = VehicleType.REGULAR
        super().save(*args, **kwargs)


class ExpressVan(Vehicle):

    max_parcel_count = models.IntegerField(
        help_text="Maximum number of parcels"
    )

    def save(self, *args, **kwargs):
        self.vehicle_type = VehicleType.EXPRESS
        super().save(*args, **kwargs)
