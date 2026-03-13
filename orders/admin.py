from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "origin",
        "destination",
        "driver",
        "vehicle",
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
