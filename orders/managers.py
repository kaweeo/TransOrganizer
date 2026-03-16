from __future__ import annotations
from typing import TYPE_CHECKING
from decimal import Decimal
from django.db import models
from django.db.models import Sum
from .choices import OrderStatus

if TYPE_CHECKING:
    from .models import Order

# Using Custom Manager + QuerySet to avoid magic string filtering
# Order.objects.filter(status="assigned", driver=driver).order_by("-created_at")
class OrderQuerySet(models.QuerySet["Order"]):

    def pending(self) -> "OrderQuerySet":
        return self.filter(status=OrderStatus.PENDING)

    def active(self) -> "OrderQuerySet":
        return self.filter(
            status__in=[
                OrderStatus.ASSIGNED,
                OrderStatus.IN_TRANSIT,
            ]
        )

    def completed(self) -> "OrderQuerySet":
        return self.filter(status=OrderStatus.DELIVERED)

    def cancelled(self) -> "OrderQuerySet":
        return self.filter(status=OrderStatus.CANCELLED)

    def recent(self) -> "OrderQuerySet":
        return self.order_by("-created_at")

    def by_driver(self, driver: models.Model) -> "OrderQuerySet":
        return self.filter(driver=driver)

    def by_vehicle(self, vehicle: models.Model) -> "OrderQuerySet":
        return self.filter(vehicle=vehicle)

    def total_revenue(self) -> Decimal:
        total = self.aggregate(total=Sum("price"))["total"]
        return total if total is not None else Decimal("0")

    def total_distance(self) -> int:
        total = self.aggregate(total=Sum("distance_km"))["total"]
        return int(total) if total is not None else 0


class OrderManager(models.Manager["Order"]):

    def get_queryset(self) -> OrderQuerySet:
        return OrderQuerySet(self.model, using=self._db)

    def pending(self) -> OrderQuerySet:
        return self.get_queryset().pending()

    def active(self) -> OrderQuerySet:
        return self.get_queryset().active()

    def completed(self) -> OrderQuerySet:
        return self.get_queryset().completed()

    def cancelled(self) -> OrderQuerySet:
        return self.get_queryset().cancelled()

    def total_revenue(self) -> Decimal:
        return self.get_queryset().total_revenue()

    def total_distance(self) -> int:
        return self.get_queryset().total_distance()
