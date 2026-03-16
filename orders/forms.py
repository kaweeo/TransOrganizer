from django import forms

from drivers.models import Driver
from vehicles.models import Vehicle
from .choices import OrderStatus
from .models import Order


class OrderCreateForm(forms.ModelForm):


    class Meta:
        model = Order

        fields = [
            "vehicle_type",
            "origin",
            "destination",
            "delivery_date",
            "distance_km",
            "cargo_weight",
            "price",
        ]

        labels = {
            "origin": "Origin Location",
            "destination": "Destination Location",
            "distance_km": "Distance (km)",
            "cargo_weight": "Cargo Weight (kg)",
            "vehicle_type": "Vehicle Type",
        }

        widgets = {
            "origin": forms.TextInput(attrs={
                "placeholder": "Sofia Warehouse"
            }),
            "destination": forms.TextInput(attrs={
                "placeholder": "Plovdiv Distribution Center"
            }),
            "delivery_date": forms.DateInput(attrs={
                "type": "date"
            }),
            "vehicle_type": forms.Select(),
        }

    def clean_distance_km(self):
        distance = self.cleaned_data.get("distance_km")

        if distance <= 0:
            raise forms.ValidationError(
                "Distance must be greater than 0."
            )

        return distance


class OrderUpdateForm(forms.ModelForm):


    class Meta:
        model = Order
        fields = "__all__"

        widgets = {
            "origin": forms.TextInput(attrs={
                "readonly": "readonly"
            }),
            "delivery_date": forms.DateInput(attrs={
                "type": "date"
            }),
        }


class OrderAssignForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = [
            "driver",
            "vehicle",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        order = self.instance
        vehicle_qs = Vehicle.objects.all()
        driver_qs = Driver.objects.all()
        if order and order.vehicle_type:
            vehicle_qs = vehicle_qs.filter(vehicle_type=order.vehicle_type)
            driver_qs = driver_qs.filter(
                vehicles__vehicle_type=order.vehicle_type
            ).distinct()

        self.fields["vehicle"].queryset = vehicle_qs
        self.fields["driver"].queryset = driver_qs
        self.fields["vehicle"].required = True
        self.fields["driver"].required = True

    def clean(self):
        cleaned_data = super().clean()
        if self.instance and self.instance.status != OrderStatus.PENDING:
            raise forms.ValidationError("Only pending orders can be assigned.")

        driver = cleaned_data.get("driver")
        vehicle = cleaned_data.get("vehicle")
        if driver and vehicle and not vehicle.drivers.filter(pk=driver.pk).exists():
            raise forms.ValidationError("Selected driver is not assigned to the chosen vehicle.")

        return cleaned_data

    def save(self, commit=True):
        order = super().save(commit=False)
        order.status = OrderStatus.ASSIGNED
        if commit:
            order.save()
            self.save_m2m()
        return order
