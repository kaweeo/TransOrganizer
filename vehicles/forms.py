from django import forms
from .models import Vehicle


class VehicleCreateForm(forms.ModelForm):


    class Meta:
        model = Vehicle

        fields = [
            "plate_number",
            "brand",
            "photo_url",
            "capacity",
            "fuel_consumption",
            "vehicle_type",
            "drivers",
        ]

        widgets = {
            "plate_number": forms.TextInput(attrs={
                "placeholder": "CA1234CB"
            }),
            "photo_url": forms.URLInput(attrs={
                "placeholder": "https://example.com/vehicle-photo.jpg"
            }),
            "drivers": forms.SelectMultiple(attrs={
                "size": 6
            }),
        }
