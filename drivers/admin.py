from django.contrib import admin
from .models import Driver


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "license_number",
        "phone_number",
        "hired_date",
    )

    search_fields = (
        "name",
        "license_number",
    )

    list_filter = (
        "hired_date",
    )
