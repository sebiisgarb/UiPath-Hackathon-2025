from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from datetime import date
from decimal import Decimal

from apps.trips.models import TripRequest, FlightOption, HotelOption, ItineraryDay


class TripPlanningAPITest(APITestCase):
    """
    Test cases for the trip planning API endpoint.
    """
    
    def test_plan_trip_with_valid_message(self):
        """Test creating a trip plan with a valid message."""
        data = {
            'message': 'I want to visit Paris next month for 5 days'
        }
        
        response = self.client.post('/api/trips/plan/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        self.assertIn('destination', response.data)
        self.assertIn('flight_options', response.data)
        self.assertIn('hotel_options', response.data)
        self.assertIn('itinerary_days', response.data)
        self.assertEqual(response.data['status'], 'completed')
    
    def test_plan_trip_without_message(self):
        """Test that message field is required."""
        data = {}
        
        response = self.client.post('/api/trips/plan/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('message', response.data)
    
    def test_plan_trip_generates_flight_options(self):
        """Test that flight options are generated."""
        data = {
            'message': 'Trip to Rome for 3 days'
        }
        
        response = self.client.post('/api/trips/plan/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertGreater(len(response.data['flight_options']), 0)
        
        # Check flight option structure
        flight = response.data['flight_options'][0]
        self.assertIn('airline', flight)
        self.assertIn('price', flight)
        self.assertIn('departure_airport', flight)
    
    def test_plan_trip_generates_hotel_options(self):
        """Test that hotel options are generated."""
        data = {
            'message': 'Visit Paris next week'
        }
        
        response = self.client.post('/api/trips/plan/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertGreater(len(response.data['hotel_options']), 0)
        
        # Check hotel option structure
        hotel = response.data['hotel_options'][0]
        self.assertIn('hotel_name', hotel)
        self.assertIn('price_per_night', hotel)
        self.assertIn('rating', hotel)
    
    def test_plan_trip_generates_itinerary(self):
        """Test that itinerary is generated."""
        data = {
            'message': 'Plan a trip to Tokyo'
        }
        
        response = self.client.post('/api/trips/plan/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertGreater(len(response.data['itinerary_days']), 0)
        
        # Check itinerary structure
        day = response.data['itinerary_days'][0]
        self.assertIn('day_number', day)
        self.assertIn('title', day)
        self.assertIn('activities', day)
    
    def test_list_trips(self):
        """Test listing all trips."""
        # Create a trip first
        TripRequest.objects.create(
            user_message='Test trip',
            destination='Paris',
            status='completed'
        )
        
        response = self.client.get('/api/trips/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
    
    def test_get_trip_detail(self):
        """Test getting trip detail."""
        trip = TripRequest.objects.create(
            user_message='Test trip',
            destination='Paris',
            status='completed'
        )
        
        response = self.client.get(f'/api/trips/{trip.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], trip.id)
        self.assertEqual(response.data['destination'], 'Paris')


class TripModelTest(TestCase):
    """
    Test cases for trip-related models.
    """
    
    def test_create_trip_request(self):
        """Test creating a trip request."""
        trip = TripRequest.objects.create(
            user_message='Visit Paris',
            destination='Paris',
            start_date=date(2024, 6, 1),
            end_date=date(2024, 6, 5),
            budget=Decimal('2000.00'),
            travelers_count=2
        )
        
        self.assertEqual(trip.destination, 'Paris')
        self.assertEqual(trip.travelers_count, 2)
        self.assertEqual(trip.status, 'pending')
    
    def test_create_flight_option(self):
        """Test creating a flight option."""
        trip = TripRequest.objects.create(
            user_message='Visit Paris',
            destination='Paris'
        )
        
        flight = FlightOption.objects.create(
            trip_request=trip,
            airline='Air France',
            flight_number='AF123',
            departure_airport='JFK',
            arrival_airport='CDG',
            departure_time='2024-06-01 10:00:00',
            arrival_time='2024-06-01 22:00:00',
            price=Decimal('500.00'),
            duration_minutes=480
        )
        
        self.assertEqual(flight.airline, 'Air France')
        self.assertEqual(trip.flight_options.count(), 1)
