from __future__ import annotations

from django.db import models
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from common.models import TimeStampedModel
from orders.choices import OrderStatus
from orders.managers import OrderManager
from orders.services import calculate_profit, calculate_transport_cost
from vehicles.models import VehicleType


class Order(TimeStampedModel):
    objects: OrderManager = OrderManager()

    origin = models.CharField(
        max_length=200,
    )

    destination = models.CharField(
        max_length=200,
    )

    delivery_date = models.DateField(
        null=True,
        blank=True
    )

    vehicle_type = models.CharField(
        max_length=20,
        choices=VehicleType,
        default=VehicleType.REGULAR,
    )

    distance_km = models.PositiveIntegerField(
        help_text="Distance between origin and destination in kilometers"
    )

    cargo_weight = models.PositiveIntegerField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Price charged to the client"
    )

    fuel_price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        help_text="Fuel price in EUR per liter at time of delivery",
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
    )

    driver = models.ForeignKey(
        "drivers.Driver",
        on_delete=models.CASCADE,
        related_name="orders",
        null=True,
        blank=True
    )
    vehicle = models.ForeignKey(
        "vehicles.Vehicle",
        on_delete=models.CASCADE,
        related_name="orders",
        null=True,
        blank=True
    )

    def transport_cost(self):
        return calculate_transport_cost(self)

    def profit(self):
        return calculate_profit(self)

    @property
    def safe_vehicle(self):
        try:
            return self.vehicle
        except ObjectDoesNotExist:
            return None

    @property
    def safe_driver(self):
        try:
            return self.driver
        except ObjectDoesNotExist:
            return None

    def __str__(self):
        return f"Order {self.id}: {self.origin} → {self.destination}"

    def clean(self):
        super().clean()
        driver = self.safe_driver
        vehicle = self.safe_vehicle
        if driver and not vehicle:
            raise ValidationError("Vehicle is required when assigning a driver.")
        if vehicle and not driver:
            raise ValidationError("Driver is required when assigning a vehicle.")
        if vehicle and vehicle.vehicle_type != self.vehicle_type:
            raise ValidationError("Assigned vehicle type must match order vehicle type.")
        if driver and vehicle and not vehicle.drivers.filter(pk=driver.pk).exists():
            raise ValidationError("Selected driver is not assigned to the chosen vehicle.")
