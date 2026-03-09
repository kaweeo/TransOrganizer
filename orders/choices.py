from django.db import models


class OrderStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    ASSIGNED = "assigned", "Assigned"
    IN_TRANSIT = "in_transit", "In Transit"
    DELIVERED = "delivered", "Delivered"
    CANCELLED = "cancelled", "Cancelled"
