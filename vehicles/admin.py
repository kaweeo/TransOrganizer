from django.contrib import admin
from .models import (
    Vehicle,
    TankTruck,
    RefrigeratedTruck,
    RegularTruck,
    ExpressVan
)


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):

    list_display = (
        "plate_number",
        "brand",
        "vehicle_type",
        "capacity",
        "fuel_consumption",
    )

    search_fields = (
        "plate_number",
        "brand",
    )

    list_filter = (
        "vehicle_type",
    )

    filter_horizontal = (
        "drivers",
    )


admin.site.register(TankTruck)
admin.site.register(RefrigeratedTruck)
admin.site.register(RegularTruck)
admin.site.register(ExpressVan)
