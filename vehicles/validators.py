from django.core.exceptions import ValidationError
import re


def validate_plate_number(value):
    """
    Validate vehicle plate number format.
    Example format: CA1234AB
    """
    pattern = r"^[A-Z]{1,2}[0-9]{3,4}[A-Z]{1,2}$"

    if not re.match(pattern, value):
        raise ValidationError(
            "Plate number must follow format like CA1234AB."
        )


def validate_fuel_consumption(value):
    if value <= 0:
        raise ValidationError(
            "Fuel consumption must be a positive number."
        )

