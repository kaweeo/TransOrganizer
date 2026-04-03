from django.db.utils import OperationalError, ProgrammingError
from django.views.generic import TemplateView

from common.models import FuelPriceSnapshot, FuelType
from .models import Order


class DashboardView(TemplateView):

    template_name = "dashboard.html"

    def _is_missing_table_error(self, exc, table_name):
        message = str(exc).lower()
        if table_name.lower() not in message:
            return False

        return any(token in message for token in ("does not exist", "no such table"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        orders = Order.objects.all().recent()

        total_profit = sum(order.profit() for order in orders)

        context["total_orders"] = orders.count()
        context["pending_orders"] = Order.objects.pending().count()
        context["completed_orders"] = Order.objects.completed().count()
        context["orders"] = orders

        context["total_revenue"] = Order.objects.total_revenue()
        context["total_distance"] = Order.objects.total_distance()
        context["total_profit"] = total_profit

        try:
            fuel_qs = FuelPriceSnapshot.objects.filter(
                country__iexact="Croatia",
                is_current=True,
            )
            latest_price = fuel_qs.order_by("-created_at").first()
            fuel_map = {item.fuel_type: item for item in fuel_qs}
        except (ProgrammingError, OperationalError) as exc:
            if self._is_missing_table_error(exc, FuelPriceSnapshot._meta.db_table):
                latest_price = None
                fuel_map = {}
            else:
                raise

        context["fuel_prices"] = {
            "gasoline": fuel_map.get(FuelType.GASOLINE),
            "diesel": fuel_map.get(FuelType.DIESEL),
        }
        context["fuel_prices_updated_at"] = latest_price.created_at if latest_price else None

        return context
