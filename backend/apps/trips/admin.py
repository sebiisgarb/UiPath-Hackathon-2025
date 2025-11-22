from django.contrib import admin
from .models import TripRequest, FlightOption, HotelOption, ItineraryDay


class FlightOptionInline(admin.TabularInline):
    model = FlightOption
    extra = 0


class HotelOptionInline(admin.TabularInline):
    model = HotelOption
    extra = 0


class ItineraryDayInline(admin.TabularInline):
    model = ItineraryDay
    extra = 0


@admin.register(TripRequest)
class TripRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'destination', 'start_date', 'end_date', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['destination', 'user_message']
    inlines = [FlightOptionInline, HotelOptionInline, ItineraryDayInline]


@admin.register(FlightOption)
class FlightOptionAdmin(admin.ModelAdmin):
    list_display = ['flight_number', 'airline', 'departure_airport', 'arrival_airport', 'price', 'is_selected']
    list_filter = ['airline', 'is_selected']


@admin.register(HotelOption)
class HotelOptionAdmin(admin.ModelAdmin):
    list_display = ['hotel_name', 'rating', 'price_per_night', 'is_selected']
    list_filter = ['rating', 'is_selected']


@admin.register(ItineraryDay)
class ItineraryDayAdmin(admin.ModelAdmin):
    list_display = ['day_number', 'date', 'title', 'trip_request']
    list_filter = ['date']
