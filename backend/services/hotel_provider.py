import random
from typing import List, Dict
from decimal import Decimal


class HotelProviderService:
    """
    Mock hotel provider service that generates hotel options.
    In production, this would integrate with real hotel APIs like Booking.com, Expedia, etc.
    """
    
    HOTEL_CHAINS = [
        'Hilton', 'Marriott', 'Hyatt', 'Sheraton', 'Westin',
        'Intercontinental', 'Radisson', 'Holiday Inn', 'Courtyard',
        'Four Seasons', 'Ritz-Carlton', 'St. Regis'
    ]
    
    HOTEL_TYPES = [
        'Hotel', 'Resort', 'Inn', 'Suites', 'Grand Hotel', 'Palace'
    ]
    
    ROOM_TYPES = [
        'Standard Room', 'Deluxe Room', 'Suite', 'Executive Suite',
        'King Room', 'Queen Room', 'Double Room'
    ]
    
    AMENITIES = [
        'Free WiFi', 'Breakfast Included', 'Pool', 'Gym', 'Spa',
        'Restaurant', 'Bar', 'Room Service', 'Concierge',
        'Airport Shuttle', 'Parking', 'Business Center'
    ]
    
    @classmethod
    def get_hotel_options(
        cls,
        destination: str,
        start_date,
        end_date,
        travelers_count: int = 1,
        preferences: Dict = None
    ) -> List[Dict]:
        """
        Generate mock hotel options for a trip.
        
        Args:
            destination: Destination city
            start_date: Check-in date
            end_date: Check-out date
            travelers_count: Number of travelers
            preferences: User preferences
            
        Returns:
            List of hotel option dictionaries
        """
        if preferences is None:
            preferences = {}
        
        hotel_options = []
        
        # Calculate number of nights
        if hasattr(start_date, 'date'):
            start_date = start_date.date()
        if hasattr(end_date, 'date'):
            end_date = end_date.date()
        
        nights = (end_date - start_date).days
        if nights <= 0:
            nights = 1
        
        # Generate 3-5 hotel options
        num_options = random.randint(3, 5)
        
        accommodation_level = preferences.get('accommodation_level', 'standard')
        
        for i in range(num_options):
            chain = random.choice(cls.HOTEL_CHAINS)
            hotel_type = random.choice(cls.HOTEL_TYPES)
            hotel_name = f"{chain} {destination} {hotel_type}"
            
            # Generate address
            street_number = random.randint(1, 999)
            street_names = ['Main St', 'Park Ave', 'Broadway', 'Central Blvd', 'Harbor Dr']
            address = f"{street_number} {random.choice(street_names)}, {destination}"
            
            # Rating (3.5 to 5.0)
            if accommodation_level == 'luxury':
                rating = round(random.uniform(4.5, 5.0), 1)
            elif accommodation_level == 'budget':
                rating = round(random.uniform(3.5, 4.2), 1)
            else:
                rating = round(random.uniform(3.8, 4.7), 1)
            
            # Room type
            room_type = random.choice(cls.ROOM_TYPES)
            
            # Price per night
            if accommodation_level == 'luxury':
                price_per_night = random.uniform(250, 600)
            elif accommodation_level == 'budget':
                price_per_night = random.uniform(70, 150)
            else:
                price_per_night = random.uniform(120, 300)
            
            # Adjust for rating
            price_per_night *= (rating / 4.0)
            
            # Adjust for travelers
            if travelers_count > 2:
                price_per_night *= 1.3
            
            price_per_night = round(price_per_night, 2)
            total_price = round(price_per_night * nights, 2)
            
            # Amenities (3-8 random amenities)
            num_amenities = random.randint(3, 8)
            amenities = random.sample(cls.AMENITIES, num_amenities)
            
            hotel_option = {
                'hotel_name': hotel_name,
                'address': address,
                'rating': Decimal(str(rating)),
                'price_per_night': Decimal(str(price_per_night)),
                'currency': 'USD',
                'total_price': Decimal(str(total_price)),
                'amenities': amenities,
                'room_type': room_type,
            }
            
            hotel_options.append(hotel_option)
        
        # Sort by price per night
        hotel_options.sort(key=lambda x: x['price_per_night'])
        
        return hotel_options
