from django.contrib import admin
from .models import Restaurant, Booking


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "cuisine",
        "rating",
        "price_range",
        "opening_time",
        "closing_time",
    )
    search_fields = ("name", "cuisine")
    list_filter = ("cuisine", "rating")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "user_name",
        "movie_title",
        "seats",
        "show_time",
    )
    search_fields = ("user_name", "movie_title")
    list_filter = ("show_time",)