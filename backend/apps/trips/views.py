from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import transaction

from .models import TripRequest, FlightOption, HotelOption, ItineraryDay
from .serializers import (
    TripRequestSerializer, 
    TripPlanRequestSerializer,
)
from services.llm_parser import LLMParserService
from services.flight_provider import FlightProviderService
from services.hotel_provider import HotelProviderService
from services.itinerary_generator import ItineraryGeneratorService


@api_view(['POST'])
def plan_trip(request):
    """
    Main endpoint for trip planning.
    
    POST /api/trips/plan/
    
    Request body:
    {
        "message": "I want to visit Paris next month for 5 days with my family"
    }
    
    This endpoint:
    1. Parses the user message using LLM parser
    2. Generates mock flight options
    3. Generates mock hotel options
    4. Generates a daily itinerary
    5. Returns the complete trip plan
    """
    # Validate request
    serializer = TripPlanRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user_message = serializer.validated_data['message']
    
    try:
        with transaction.atomic():
            # Step 1: Parse the message
            parsed_data = LLMParserService.parse_message(user_message)
            
            # Create trip request
            trip_request = TripRequest.objects.create(
                user_message=user_message,
                destination=parsed_data.get('destination', 'Unknown'),
                start_date=parsed_data.get('start_date'),
                end_date=parsed_data.get('end_date'),
                budget=parsed_data.get('budget'),
                travelers_count=parsed_data.get('travelers_count', 1),
                preferences=parsed_data.get('preferences', {}),
                status='processing'
            )
            
            # Step 2: Generate flight options
            if trip_request.destination and trip_request.start_date:
                flight_options_data = FlightProviderService.get_flight_options(
                    destination=trip_request.destination,
                    start_date=trip_request.start_date,
                    travelers_count=trip_request.travelers_count
                )
                
                # Save flight options
                for flight_data in flight_options_data:
                    FlightOption.objects.create(
                        trip_request=trip_request,
                        **flight_data
                    )
            
            # Step 3: Generate hotel options
            if trip_request.destination and trip_request.start_date and trip_request.end_date:
                hotel_options_data = HotelProviderService.get_hotel_options(
                    destination=trip_request.destination,
                    start_date=trip_request.start_date,
                    end_date=trip_request.end_date,
                    travelers_count=trip_request.travelers_count,
                    preferences=trip_request.preferences
                )
                
                # Save hotel options
                for hotel_data in hotel_options_data:
                    HotelOption.objects.create(
                        trip_request=trip_request,
                        **hotel_data
                    )
            
            # Step 4: Generate itinerary
            if trip_request.destination and trip_request.start_date and trip_request.end_date:
                itinerary_data = ItineraryGeneratorService.generate_itinerary(
                    destination=trip_request.destination,
                    start_date=trip_request.start_date,
                    end_date=trip_request.end_date,
                    preferences=trip_request.preferences
                )
                
                # Save itinerary days
                for day_data in itinerary_data:
                    ItineraryDay.objects.create(
                        trip_request=trip_request,
                        **day_data
                    )
            
            # Update status to completed
            trip_request.status = 'completed'
            trip_request.save()
            
            # Return the complete trip plan
            response_serializer = TripRequestSerializer(trip_request)
            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED
            )
    
    except Exception as e:
        # If anything fails, mark as failed and return error
        if 'trip_request' in locals():
            trip_request.status = 'failed'
            trip_request.save()
        
        return Response(
            {
                'error': 'Failed to create trip plan',
                'detail': str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def list_trips(request):
    """
    List all trip requests.
    
    GET /api/trips/
    """
    trips = TripRequest.objects.all()
    serializer = TripRequestSerializer(trips, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_trip_detail(request, trip_id):
    """
    Get details of a specific trip.
    
    GET /api/trips/{trip_id}/
    """
    try:
        trip = TripRequest.objects.get(id=trip_id)
        serializer = TripRequestSerializer(trip)
        return Response(serializer.data)
    except TripRequest.DoesNotExist:
        return Response(
            {'error': 'Trip not found'},
            status=status.HTTP_404_NOT_FOUND
        )
