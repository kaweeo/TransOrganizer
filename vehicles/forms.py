from django import forms
from .models import Vehicle


class VehicleCreateForm(forms.ModelForm):


    class Meta:
        model = Vehicle

        fields = [
            "plate_number",
            "brand",
            "capacity",
            "fuel_consumption",
            "vehicle_type",
            "drivers",
        ]

        widgets = {
            "plate_number": forms.TextInput(attrs={
                "placeholder": "CA1234CB"
            }),
            "drivers": forms.SelectMultiple(attrs={
                "size": 6
            }),
        }
