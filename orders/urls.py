from django.urls import path

from .view_dashboard import DashboardView
from .views import (
    OrderListView,
    OrderCreateView,
    OrderDetailView,
    OrderUpdateView,
    OrderDeleteView,
    OrderAssignView,
)

urlpatterns = [
    path("", OrderListView.as_view(), name="order-list"),
    path("create/", OrderCreateView.as_view(), name="order-create"),
    path("<int:pk>/", OrderDetailView.as_view(), name="order-detail"),
    path("<int:pk>/edit/", OrderUpdateView.as_view(), name="order-update"),
    path("<int:pk>/assign/", OrderAssignView.as_view(), name="order-assign"),
    path("<int:pk>/delete/", OrderDeleteView.as_view(), name="order-delete"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
]
