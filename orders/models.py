from __future__ import annotations

from django.db import models

from common.models import TimeStampedModel
from orders.choices import OrderStatus
from orders.managers import OrderManager
from orders.services import calculate_profit, calculate_transport_cost


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
        help_text="Fuel price in EUR per liter at time of delivery"
    )

    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
    )

    driver = models.ForeignKey(
        "drivers.Driver",
        on_delete=models.CASCADE,
        related_name="orders"
    )
    vehicle = models.ForeignKey(
        "vehicles.Vehicle",
        on_delete=models.CASCADE,
        related_name="orders"
    )

    def transport_cost(self):
        return calculate_transport_cost(self)

    def profit(self):
        return calculate_profit(self)

    def __str__(self):
        return f"Order {self.id}: {self.origin} → {self.destination}"
