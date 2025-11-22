import random
from datetime import datetime, timedelta
from typing import List, Dict
from decimal import Decimal


class FlightProviderService:
    """
    Mock flight provider service that generates flight options.
    In production, this would integrate with real flight APIs like Amadeus, Skyscanner, etc.
    """
    
    AIRLINES = [
        'American Airlines', 'Delta Airlines', 'United Airlines', 
        'Southwest Airlines', 'JetBlue', 'Alaska Airlines',
        'Lufthansa', 'British Airways', 'Air France', 'Emirates'
    ]
    
    AIRPORTS = {
        'New York': ['JFK', 'LGA', 'EWR'],
        'Los Angeles': ['LAX', 'BUR', 'SNA'],
        'Chicago': ['ORD', 'MDW'],
        'Paris': ['CDG', 'ORY'],
        'London': ['LHR', 'LGW', 'STN'],
        'Tokyo': ['NRT', 'HND'],
        'Rome': ['FCO', 'CIA'],
        'Barcelona': ['BCN'],
        'Dubai': ['DXB'],
        'Singapore': ['SIN'],
    }
    
    @classmethod
    def get_flight_options(
        cls, 
        destination: str, 
        start_date: datetime.date,
        travelers_count: int = 1,
        origin: str = "New York"
    ) -> List[Dict]:
        """
        Generate mock flight options for a trip.
        
        Args:
            destination: Destination city
            start_date: Departure date
            travelers_count: Number of travelers
            origin: Origin city
            
        Returns:
            List of flight option dictionaries
        """
        flight_options = []
        
        # Get airports
        origin_airports = cls.AIRPORTS.get(origin, ['JFK'])
        dest_airports = cls.AIRPORTS.get(destination, ['INT'])
        
        # Generate 3-5 flight options
        num_options = random.randint(3, 5)
        
        for i in range(num_options):
            airline = random.choice(cls.AIRLINES)
            flight_number = f"{random.choice(['AA', 'DL', 'UA', 'BA', 'LH'])}{random.randint(100, 999)}"
            
            departure_airport = random.choice(origin_airports)
            arrival_airport = random.choice(dest_airports)
            
            # Generate departure time (between 6 AM and 10 PM)
            departure_hour = random.randint(6, 22)
            departure_minute = random.choice([0, 15, 30, 45])
            departure_time = datetime.combine(
                start_date, 
                datetime.min.time().replace(hour=departure_hour, minute=departure_minute)
            )
            
            # Duration between 2-14 hours depending on distance
            duration_minutes = random.randint(120, 840)
            arrival_time = departure_time + timedelta(minutes=duration_minutes)
            
            # Number of stops
            stops = random.choice([0, 0, 0, 1, 1, 2])  # Weighted towards non-stop
            
            # Price calculation (base price + factors)
            base_price = 200 + (duration_minutes / 60) * 50
            if stops == 0:
                base_price *= 1.3
            elif stops == 2:
                base_price *= 0.7
            
            # Add some randomness
            price = base_price * random.uniform(0.8, 1.4)
            price = round(price * travelers_count, 2)
            
            flight_option = {
                'airline': airline,
                'flight_number': flight_number,
                'departure_airport': departure_airport,
                'arrival_airport': arrival_airport,
                'departure_time': departure_time,
                'arrival_time': arrival_time,
                'price': Decimal(str(price)),
                'currency': 'USD',
                'duration_minutes': duration_minutes,
                'stops': stops,
            }
            
            flight_options.append(flight_option)
        
        # Sort by price
        flight_options.sort(key=lambda x: x['price'])
        
        return flight_options
