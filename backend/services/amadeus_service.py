"""
Amadeus API Service - Complete wrapper for Amadeus Self-Service APIs
Based on https://github.com/amadeus4dev/amadeus-code-examples

This service provides functions for:
- Flight search and booking
- Hotel search and booking
- Tours & Activities
- Points of Interest
- Airport/City search
- Transfer search
- Travel recommendations
"""

import os
from typing import Optional, List, Dict, Any
from amadeus import Client, ResponseError, Location


class AmadeusService:
    """
    Comprehensive Amadeus API service wrapper.
    Uses the official Amadeus Python SDK.
    """
    
    def __init__(self, client_id: Optional[str] = None, client_secret: Optional[str] = None, hostname: str = 'test'):
        """
        Initialize Amadeus client.
        
        Args:
            client_id: Amadeus API client ID (defaults to env var AMADEUS_CLIENT_ID)
            client_secret: Amadeus API client secret (defaults to env var AMADEUS_CLIENT_SECRET)
            hostname: 'test' or 'production' (defaults to env var AMADEUS_HOSTNAME or 'test')
        """
        self.client_id = client_id or os.getenv('AMADEUS_CLIENT_ID')
        self.client_secret = client_secret or os.getenv('AMADEUS_CLIENT_SECRET')
        self.hostname = hostname or os.getenv('AMADEUS_HOSTNAME', 'test')
        
        if not self.client_id or not self.client_secret:
            raise ValueError("Amadeus API credentials not provided. Set AMADEUS_CLIENT_ID and AMADEUS_CLIENT_SECRET environment variables.")
        
        self.client = Client(
            client_id=self.client_id,
            client_secret=self.client_secret,
            hostname=self.hostname
        )
    
    # ==================== FLIGHT APIS ====================
    
    def search_flights(
        self,
        origin: str,
        destination: str,
        departure_date: str,
        adults: int = 1,
        return_date: Optional[str] = None,
        children: int = 0,
        infants: int = 0,
        travel_class: Optional[str] = None,
        non_stop: bool = False,
        currency: str = 'USD',
        max_results: int = 250
    ) -> Dict[str, Any]:
        """
        Search for flight offers.
        
        Args:
            origin: IATA code of origin airport (e.g., 'JFK')
            destination: IATA code of destination airport (e.g., 'CDG')
            departure_date: Departure date in YYYY-MM-DD format
            adults: Number of adult travelers (12+ years)
            return_date: Return date in YYYY-MM-DD format (for round trip)
            children: Number of children (2-11 years)
            infants: Number of infants (under 2 years)
            travel_class: 'ECONOMY', 'PREMIUM_ECONOMY', 'BUSINESS', or 'FIRST'
            non_stop: Only return non-stop flights
            currency: Currency code (default: USD)
            max_results: Maximum number of results
            
        Returns:
            Dictionary with flight offers data
        """
        try:
            params = {
                'originLocationCode': origin,
                'destinationLocationCode': destination,
                'departureDate': departure_date,
                'adults': adults,
                'currencyCode': currency,
                'max': max_results
            }
            
            if return_date:
                params['returnDate'] = return_date
            if children > 0:
                params['children'] = children
            if infants > 0:
                params['infants'] = infants
            if travel_class:
                params['travelClass'] = travel_class
            if non_stop:
                params['nonStop'] = 'true'
            
            response = self.client.shopping.flight_offers_search.get(**params)
            return {'success': True, 'data': response.data}
        except ResponseError as error:
            return {'success': False, 'error': str(error)}
    
    def get_flight_cheapest_dates(
        self,
        origin: str,
        destination: str,
        departure_date: Optional[str] = None,
        one_way: bool = False
    ) -> Dict[str, Any]:
        """
        Find the cheapest dates to fly.
        
        Args:
            origin: IATA code of origin airport
            destination: IATA code of destination airport
            departure_date: Optional departure date (finds cheapest around this date)
            one_way: True for one-way, False for round-trip
            
        Returns:
            Dictionary with cheapest flight dates
        """
        try:
            params = {
                'origin': origin,
                'destination': destination,
                'oneWay': one_way
            }
            if departure_date:
                params['departureDate'] = departure_date
                
            response = self.client.shopping.flight_dates.get(**params)
            return {'success': True, 'data': response.data}
        except ResponseError as error:
            return {'success': False, 'error': str(error)}
    
    def predict_flight_delay(
        self,
        origin: str,
        destination: str,
        departure_date: str,
        departure_time: str,
        arrival_date: str,
        arrival_time: str,
        airline_code: str,
        flight_number: str
    ) -> Dict[str, Any]:
        """
        Predict the likelihood of a flight being delayed.
        
        Args:
            origin: Origin airport IATA code
            destination: Destination airport IATA code
            departure_date: Date in YYYY-MM-DD format
            departure_time: Time in HH:MM:SS format
            arrival_date: Date in YYYY-MM-DD format
            arrival_time: Time in HH:MM:SS format
            airline_code: 2-character airline IATA code
            flight_number: Flight number
            
        Returns:
            Dictionary with delay prediction
        """
        try:
            response = self.client.travel.predictions.flight_delay.get(
                originLocationCode=origin,
                destinationLocationCode=destination,
                departureDate=departure_date,
                departureTime=departure_time,
                arrivalDate=arrival_date,
                arrivalTime=arrival_time,
                aircraftCode=airline_code,
                flightNumber=flight_number
            )
            return {'success': True, 'data': response.data}
        except ResponseError as error:
            return {'success': False, 'error': str(error)}
    
    # ==================== HOTEL APIS ====================
    
    def search_hotels_by_city(
        self,
        city_code: str,
        check_in_date: str,
        check_out_date: str,
        adults: int = 1,
        room_quantity: int = 1,
        currency: str = 'USD',
        radius: int = 5,
        radius_unit: str = 'KM'
    ) -> Dict[str, Any]:
        """
        Search for hotels in a city.
        
        Args:
            city_code: IATA city code (e.g., 'PAR' for Paris)
            check_in_date: Check-in date in YYYY-MM-DD format
            check_out_date: Check-out date in YYYY-MM-DD format
            adults: Number of adult guests per room
            room_quantity: Number of rooms
            currency: Currency code
            radius: Search radius
            radius_unit: 'KM' or 'MILE'
            
        Returns:
            Dictionary with hotel offers
        """
        try:
            response = self.client.shopping.hotel_offers_search.get(
                cityCode=city_code,
                checkInDate=check_in_date,
                checkOutDate=check_out_date,
                adults=adults,
                roomQuantity=room_quantity,
                currency=currency,
                radius=radius,
                radiusUnit=radius_unit
            )
            return {'success': True, 'data': response.data}
        except ResponseError as error:
            return {'success': False, 'error': str(error)}
    
    def search_hotels_by_hotels(
        self,
        hotel_ids: List[str],
        check_in_date: str,
        check_out_date: str,
        adults: int = 1,
        room_quantity: int = 1,
        currency: str = 'USD'
    ) -> Dict[str, Any]:
        """
        Search for specific hotels by their IDs.
        
        Args:
            hotel_ids: List of Amadeus hotel IDs
            check_in_date: Check-in date in YYYY-MM-DD format
            check_out_date: Check-out date in YYYY-MM-DD format
            adults: Number of adult guests per room
            room_quantity: Number of rooms
            currency: Currency code
            
        Returns:
            Dictionary with hotel offers
        """
        try:
            response = self.client.shopping.hotel_offers_search.get(
                hotelIds=','.join(hotel_ids),
                checkInDate=check_in_date,
                checkOutDate=check_out_date,
                adults=adults,
                roomQuantity=room_quantity,
                currency=currency
            )
            return {'success': True, 'data': response.data}
        except ResponseError as error:
            return {'success': False, 'error': str(error)}
    
    def get_hotel_offer(self, offer_id: str) -> Dict[str, Any]:
        """
        Get details of a specific hotel offer.
        
        Args:
            offer_id: Amadeus hotel offer ID
            
        Returns:
            Dictionary with hotel offer details
        """
        try:
            response = self.client.shopping.hotel_offer_search(offer_id).get()
            return {'success': True, 'data': response.data}
        except ResponseError as error:
            return {'success': False, 'error': str(error)}
    
    def get_hotel_ratings(
        self,
        hotel_ids: List[str]
    ) -> Dict[str, Any]:
        """
        Get sentiment analysis ratings for hotels.
        
        Args:
            hotel_ids: List of Amadeus hotel IDs (max 3)
            
        Returns:
            Dictionary with hotel ratings
        """
        try:
            response = self.client.e_reputation.hotel_sentiments.get(
                hotelIds=','.join(hotel_ids[:3])  # Max 3 hotels
            )
            return {'success': True, 'data': response.data}
        except ResponseError as error:
            return {'success': False, 'error': str(error)}
    
    def search_hotel_by_name(
        self,
        keyword: str,
        sub_type: List[str] = None
    ) -> Dict[str, Any]:
        """
        Search hotels by name (autocomplete).
        
        Args:
            keyword: Search keyword (hotel name)
            sub_type: List of location subtypes (e.g., ['HOTEL_LEISURE', 'HOTEL_GDS'])
            
        Returns:
            Dictionary with matching hotels
        """
        try:
            params = {'keyword': keyword}
            if sub_type:
                params['subType'] = ','.join(sub_type)
            
            response = self.client.reference_data.locations.get(**params)
            return {'success': True, 'data': response.data}
        except ResponseError as error:
            return {'success': False, 'error': str(error)}
    
    # ==================== ACTIVITIES & POI APIS ====================
    
    def search_activities(
        self,
        latitude: float,
        longitude: float,
        radius: int = 1
    ) -> Dict[str, Any]:
        """
        Search for tours and activities by location.
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            radius: Search radius in km (1-20)
            
        Returns:
            Dictionary with activities data
        """
        try:
            response = self.client.shopping.activities.get(
                latitude=latitude,
                longitude=longitude,
                radius=radius
            )
            return {'success': True, 'data': response.data}
        except ResponseError as error:
            return {'success': False, 'error': str(error)}
    
    def get_activity_details(self, activity_id: str) -> Dict[str, Any]:
        """
        Get details of a specific activity.
        
        Args:
            activity_id: Amadeus activity ID
            
        Returns:
            Dictionary with activity details
        """
        try:
            response = self.client.shopping.activity(activity_id).get()
            return {'success': True, 'data': response.data}
        except ResponseError as error:
            return {'success': False, 'error': str(error)}
    
    def search_points_of_interest(
        self,
        latitude: float,
        longitude: float,
        radius: int = 1,
        categories: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Search for points of interest (landmarks, attractions).
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            radius: Search radius in km
            categories: List of POI categories (e.g., ['SIGHTS', 'NIGHTLIFE', 'RESTAURANT'])
            
        Returns:
            Dictionary with POIs
        """
        try:
            params = {
                'latitude': latitude,
                'longitude': longitude,
                'radius': radius
            }
            if categories:
                params['categories'] = ','.join(categories)
            
            response = self.client.reference_data.locations.points_of_interest.get(**params)
            return {'success': True, 'data': response.data}
        except ResponseError as error:
            return {'success': False, 'error': str(error)}
    
    def get_poi_details(self, poi_id: str) -> Dict[str, Any]:
        """
        Get details of a specific point of interest.
        
        Args:
            poi_id: POI ID
            
        Returns:
            Dictionary with POI details
        """
        try:
            response = self.client.reference_data.locations.point_of_interest(poi_id).get()
            return {'success': True, 'data': response.data}
        except ResponseError as error:
            return {'success': False, 'error': str(error)}
    
    # ==================== LOCATION APIS ====================
    
    def search_locations(
        self,
        keyword: str,
        sub_type: Optional[List[str]] = None,
        view: str = 'FULL'
    ) -> Dict[str, Any]:
        """
        Search for airports, cities, and locations.
        
        Args:
            keyword: Search keyword
            sub_type: List of location types (e.g., ['AIRPORT', 'CITY'])
            view: 'LIGHT' or 'FULL'
            
        Returns:
            Dictionary with matching locations
        """
        try:
            params = {'keyword': keyword, 'view': view}
            
            # Handle subType parameter
            if sub_type:
                # Convert list to proper format
                sub_type_value = [getattr(Location, st, st) for st in sub_type]
                params['subType'] = sub_type_value
            
            response = self.client.reference_data.locations.get(**params)
            return {'success': True, 'data': response.data}
        except ResponseError as error:
            return {'success': False, 'error': str(error)}
    
    def get_location_details(self, location_id: str) -> Dict[str, Any]:
        """
        Get details of a specific location.
        
        Args:
            location_id: Location ID
            
        Returns:
            Dictionary with location details
        """
        try:
            response = self.client.reference_data.location(location_id).get()
            return {'success': True, 'data': response.data}
        except ResponseError as error:
            return {'success': False, 'error': str(error)}
    
    def search_airports(
        self,
        latitude: float,
        longitude: float,
        radius: int = 500
    ) -> Dict[str, Any]:
        """
        Search for nearest airports by coordinates.
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            radius: Search radius in km
            
        Returns:
            Dictionary with nearby airports
        """
        try:
            response = self.client.reference_data.locations.airports.get(
                latitude=latitude,
                longitude=longitude,
                radius=radius
            )
            return {'success': True, 'data': response.data}
        except ResponseError as error:
            return {'success': False, 'error': str(error)}
    
    # ==================== TRANSFER APIS ====================
    
    def search_transfers(
        self,
        start_latitude: float,
        start_longitude: float,
        end_latitude: float,
        end_longitude: float,
        start_date_time: str,
        passengers: int = 1,
        start_address_line: Optional[str] = None,
        end_address_line: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Search for ground transfers (taxis, shuttles, private cars).
        
        Args:
            start_latitude: Starting point latitude
            start_longitude: Starting point longitude
            end_latitude: Destination latitude
            end_longitude: Destination longitude
            start_date_time: Pickup date/time in ISO format
            passengers: Number of passengers
            start_address_line: Starting address (optional)
            end_address_line: Destination address (optional)
            
        Returns:
            Dictionary with transfer options
        """
        try:
            body = {
                'startLocationCode': f'{start_latitude},{start_longitude}',
                'endLocationCode': f'{end_latitude},{end_longitude}',
                'transferType': 'PRIVATE',
                'startDateTime': start_date_time,
                'passengers': passengers
            }
            
            if start_address_line:
                body['startAddressLine'] = start_address_line
            if end_address_line:
                body['endAddressLine'] = end_address_line
            
            response = self.client.shopping.transfer_offers.post(body)
            return {'success': True, 'data': response.data}
        except ResponseError as error:
            return {'success': False, 'error': str(error)}
    
    # ==================== RECOMMENDATIONS APIS ====================
    
    def get_travel_recommendations(
        self,
        origin: str,
        destination_country: Optional[str] = None,
        max_results: int = 10
    ) -> Dict[str, Any]:
        """
        Get AI-powered travel destination recommendations.
        
        Args:
            origin: Origin city IATA code
            destination_country: Optional destination country code (ISO 3166-1 alpha-2)
            max_results: Maximum number of recommendations
            
        Returns:
            Dictionary with recommended destinations
        """
        try:
            params = {'cityCodes': origin, 'max': max_results}
            if destination_country:
                params['destinationCountryCodes'] = destination_country
            
            response = self.client.reference_data.recommended_locations.get(**params)
            return {'success': True, 'data': response.data}
        except ResponseError as error:
            return {'success': False, 'error': str(error)}
    
    # ==================== AIRLINE & AIRPORT INFO ====================
    
    def lookup_airline(self, airline_code: str) -> Dict[str, Any]:
        """
        Look up airline information by code.
        
        Args:
            airline_code: 2-letter IATA airline code
            
        Returns:
            Dictionary with airline information
        """
        try:
            response = self.client.reference_data.airlines.get(airlineCodes=airline_code)
            return {'success': True, 'data': response.data}
        except ResponseError as error:
            return {'success': False, 'error': str(error)}
    
    def get_airport_routes(
        self,
        airport_code: str,
        max_results: int = 50
    ) -> Dict[str, Any]:
        """
        Get all routes departing from an airport.
        
        Args:
            airport_code: 3-letter IATA airport code
            max_results: Maximum number of routes
            
        Returns:
            Dictionary with airport routes
        """
        try:
            response = self.client.airport.direct_destinations.get(
                departureAirportCode=airport_code,
                max=max_results
            )
            return {'success': True, 'data': response.data}
        except ResponseError as error:
            return {'success': False, 'error': str(error)}
