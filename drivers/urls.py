from django.urls import path
from .views import (
    DriverListView,
    DriverCreateView,
    DriverDetailView,
    DriverUpdateView,
    DriverDeleteView,
)

urlpatterns = [
    path("", DriverListView.as_view(), name="driver-list"),
    path("create/", DriverCreateView.as_view(), name="driver-create"),
    path("<int:pk>/", DriverDetailView.as_view(), name="driver-detail"),
    path("<int:pk>/edit/", DriverUpdateView.as_view(), name="driver-update"),
    path("<int:pk>/delete/", DriverDeleteView.as_view(), name="driver-delete"),
]
