from django import forms
from .models import Vehicle


class VehicleCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        drivers_field = self.fields.get("drivers")
        if drivers_field:
            drivers_field.required = False
            if not self.instance.pk:
                drivers_field.initial = []


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
