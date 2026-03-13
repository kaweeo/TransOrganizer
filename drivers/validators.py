import re

from django.core.exceptions import ValidationError


_E164_PATTERN = re.compile(r"^\+[1-9]\d{7,14}$")


def validate_phone_number(value: str) -> None:
    """Validate international phone numbers in strict E.164 format.
    Example: +359888123456
    """
    if value is None:
        raise ValidationError("Phone number is required.")

    phone = value.strip()
    if not _E164_PATTERN.match(phone):
        raise ValidationError(
            "Enter a valid phone number in E.164 format (e.g. +359888123456)."
        )
