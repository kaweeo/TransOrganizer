from django.shortcuts import render
from django.urls import reverse_lazy

from common.views import (
    BaseListView,
    BaseCreateView,
    BaseDetailView,
    BaseUpdateView,
    BaseDeleteView,
)

from .models import Vehicle
from .forms import VehicleCreateForm


class VehicleListView(BaseListView):
    model = Vehicle
    template_name = "vehicles/vehicle_list.html"
    context_object_name = "vehicles"


class VehicleDetailView(BaseDetailView):
    model = Vehicle
    template_name = "vehicles/vehicle_detail.html"
    context_object_name = "vehicle"


class VehicleCreateView(BaseCreateView):
    model = Vehicle
    form_class = VehicleCreateForm
    template_name = "vehicles/vehicle_create.html"
    success_url = reverse_lazy("vehicle-list")


class VehicleUpdateView(BaseUpdateView):
    model = Vehicle
    form_class = VehicleCreateForm
    template_name = "vehicles/vehicle_update.html"
    success_url = reverse_lazy("vehicle-list")


class VehicleDeleteView(BaseDeleteView):
    model = Vehicle
    template_name = "vehicles/vehicle_delete.html"
    success_url = reverse_lazy("vehicle-list")

