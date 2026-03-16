from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "origin",
        "destination",
        "safe_driver",
        "safe_vehicle",
        "status",
        "delivery_date",
    )

    search_fields = (
        "origin",
        "destination",
    )

    list_filter = (
        "status",
        "delivery_date",
    )

    autocomplete_fields = (
        "driver",
        "vehicle",
    )

    @admin.display(description="Driver")
    def safe_driver(self, obj):
        return obj.safe_driver or "-"

    @admin.display(description="Vehicle")
    def safe_vehicle(self, obj):
        return obj.safe_vehicle or "-"
