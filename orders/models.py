from django.db import models


class Order(models.Model):
    origin = models.CharField(
        max_length=200,
    )
    destination = models.CharField(
        max_length=200,
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
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def transport_cost(self):
        """
        Calculate fuel cost for the trip.
        """
        liters_used = (self.distance_km / 100) * self.vehicle.fuel_consumption
        return liters_used * float(self.fuel_price)

    def profit(self):
        return float(self.price) - self.transport_cost()

    def __str__(self):
        return f"Order {self.id}: {self.origin} → {self.destination}"
