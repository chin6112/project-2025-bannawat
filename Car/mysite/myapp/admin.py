from django.contrib import admin
from .models import Car, Driver, ShuttleRequest

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ("license_plate", "name", "active")
    list_filter = ("active",)
    search_fields = ("license_plate", "name")


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ("name", "phone")
    search_fields = ("name", "phone")


@admin.register(ShuttleRequest)
class ShuttleRequestAdmin(admin.ModelAdmin):
    list_display = ("user_name", "pickup_location", "dropoff_location",
                    "start_time", "status", "car", "driver")
    list_filter = ("status", "car", "driver")
    search_fields = ("user_name", "pickup_location", "dropoff_location")
    ordering = ("-start_time",)
