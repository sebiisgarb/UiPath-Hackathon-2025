from rest_framework import serializers
from .models import TripRequest, FlightOption, HotelOption, ItineraryDay


class FlightOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlightOption
        fields = [
            'id', 'airline', 'flight_number', 'departure_airport', 
            'arrival_airport', 'departure_time', 'arrival_time', 
            'price', 'currency', 'duration_minutes', 'stops', 'is_selected'
        ]


class HotelOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelOption
        fields = [
            'id', 'hotel_name', 'address', 'rating', 'price_per_night', 
            'currency', 'total_price', 'amenities', 'room_type', 'is_selected'
        ]


class ItineraryDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = ItineraryDay
        fields = ['id', 'day_number', 'date', 'title', 'description', 'activities']


class TripRequestSerializer(serializers.ModelSerializer):
    flight_options = FlightOptionSerializer(many=True, read_only=True)
    hotel_options = HotelOptionSerializer(many=True, read_only=True)
    itinerary_days = ItineraryDaySerializer(many=True, read_only=True)
    
    class Meta:
        model = TripRequest
        fields = [
            'id', 'user_message', 'destination', 'start_date', 'end_date', 
            'budget', 'travelers_count', 'preferences', 'status', 
            'created_at', 'updated_at', 'flight_options', 'hotel_options', 
            'itinerary_days'
        ]
        read_only_fields = ['status', 'created_at', 'updated_at']


class TripPlanRequestSerializer(serializers.Serializer):
    """
    Serializer for the trip planning request endpoint.
    """
    message = serializers.CharField(
        required=True,
        help_text="User's trip planning message or query"
    )
