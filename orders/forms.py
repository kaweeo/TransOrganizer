from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):


    class Meta:
        model = Order

        fields = [
            "origin",
            "destination",
            "delivery_date",
            "distance_km",
            "cargo_weight",
            "price",
            "fuel_price",
            "status",
            "driver",
            "vehicle",
        ]

        labels = {
            "origin": "Origin Location",
            "destination": "Destination Location",
            "distance_km": "Distance (km)",
            "cargo_weight": "Cargo Weight (kg)",
            "fuel_price": "Fuel Price (EUR/L)",
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
