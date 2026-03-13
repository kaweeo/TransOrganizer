from django import forms
from .models import Driver
from .validators import validate_phone_number


class DriverCreateForm(forms.ModelForm):


    class Meta:
        model = Driver
        fields = [
            "name",
            "license_number",
            "phone_number",
            "hired_date",
        ]

        labels = {
            "name": "Driver Name",
            "license_number": "License Number",
            "phone_number": "Phone Number",
            "hired_date": "Hire Date",
        }

        help_texts = {
            "license_number": "Please double check your driver license number"
        }

        widgets = {
            "name": forms.TextInput(
                attrs={
                "placeholder": "Ivan Petrov"
                }
            ),
            "license_number": forms.TextInput(
                attrs={
                "placeholder": "0123456789"
                }
            ),
            "phone_number": forms.TextInput(
                attrs={
                "placeholder": "+359888123456"
                }
            ),
            "hired_date": forms.DateInput(
                attrs={
                "type": "date"
                }
            ),
        }

    def clean_phone_number(self):

        phone = self.cleaned_data.get("phone_number")
        validate_phone_number(phone)

        return phone


class DriverUpdateForm(forms.ModelForm):

    class Meta:
        model = Driver
        fields = "__all__"

        widgets = {
            "license_number": forms.TextInput(
                attrs={
                "readonly": "readonly"              # 'read-only field' requirement
            }
            ),
            "hired_date": forms.DateInput(attrs={
                "type": "date"
            }),
        }
