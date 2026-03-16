from django.shortcuts import render
from django.urls import reverse, reverse_lazy

from common.views import (
    BaseListView,
    BaseCreateView,
    BaseDetailView,
    BaseUpdateView,
    BaseDeleteView,
)

from .models import Order
from .choices import OrderStatus
from .forms import OrderCreateForm, OrderUpdateForm, OrderAssignForm


class OrderListView(BaseListView):
    model = Order
    template_name = "orders/order_list.html"
    context_object_name = "orders"

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get("status")
        if status in OrderStatus.values:
            queryset = queryset.filter(status=status)

        order_by = self.request.GET.get("order_by")
        allowed = {
            "created_at",
            "-created_at",
            "delivery_date",
            "-delivery_date",
            "price",
            "-price",
            "distance_km",
            "-distance_km",
        }
        if order_by in allowed:
            queryset = queryset.order_by(order_by)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_status"] = self.request.GET.get("status", "")
        context["current_order_by"] = self.request.GET.get("order_by", "")
        context["status_choices"] = OrderStatus.choices
        return context


class OrderCreateView(BaseCreateView):
    model = Order
    form_class = OrderCreateForm
    template_name = "orders/order_create.html"
    success_url = reverse_lazy("order-list")


class OrderDetailView(BaseDetailView):
    model = Order
    template_name = "orders/order_detail.html"
    context_object_name = "order"


class OrderUpdateView(BaseUpdateView):
    model = Order
    form_class = OrderUpdateForm
    template_name = "orders/order_update.html"
    success_url = reverse_lazy("order-list")


class OrderDeleteView(BaseDeleteView):
    model = Order
    template_name = "orders/order_delete.html"
    success_url = reverse_lazy("order-list")


class OrderAssignView(BaseUpdateView):
    model = Order
    form_class = OrderAssignForm
    template_name = "orders/order_assign.html"
    context_object_name = "order"

    def get_queryset(self):
        return super().get_queryset().pending()

    def get_success_url(self):
        return reverse("order-detail", kwargs={"pk": self.object.pk})
