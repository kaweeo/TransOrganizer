from decimal import Decimal

from django.shortcuts import render
from django.urls import reverse_lazy

from common.views import (
    BaseListView,
    BaseCreateView,
    BaseDetailView,
    BaseUpdateView,
    BaseDeleteView,
)

from .models import Driver
from .forms import DriverCreateForm, DriverUpdateForm
from orders.models import Order


class DriverListView(BaseListView):
    model = Driver
    template_name = "drivers/driver_list.html"
    context_object_name = "drivers"


class DriverCreateView(BaseCreateView):
    model = Driver
    form_class = DriverCreateForm
    template_name = "drivers/driver_create.html"
    success_url = reverse_lazy("driver-list")


class DriverDetailView(BaseDetailView):
    model = Driver
    template_name = "drivers/driver_detail.html"
    context_object_name = "driver"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        driver = self.object
        orders = Order.objects.filter(driver=driver)
        revenue = sum((order.price or Decimal("0")) for order in orders)
        profit = sum(order.profit() for order in orders)
        context["driver_revenue"] = revenue
        context["driver_profit"] = profit
        context["driver_order_count"] = orders.count()
        return context


class DriverUpdateView(BaseUpdateView):
    model = Driver
    form_class = DriverUpdateForm
    template_name = "drivers/driver_update.html"
    success_url = reverse_lazy("driver-list")


class DriverDeleteView(BaseDeleteView):
    model = Driver
    template_name = "drivers/driver_delete.html"
    success_url = reverse_lazy("driver-list")
