import random
from datetime import timedelta
from typing import List, Dict


class ItineraryGeneratorService:
    """
    Service to generate daily itineraries for trips.
    In production, this would use an LLM to generate personalized itineraries.
    """
    
    CITY_ATTRACTIONS = {
        'Paris': [
            'Eiffel Tower', 'Louvre Museum', 'Notre-Dame Cathedral', 
            'Arc de Triomphe', 'Sacré-Cœur', 'Champs-Élysées',
            'Versailles Palace', 'Musée d\'Orsay'
        ],
        'London': [
            'Big Ben', 'Tower of London', 'British Museum', 
            'Buckingham Palace', 'London Eye', 'Westminster Abbey',
            'Tower Bridge', 'Hyde Park'
        ],
        'Rome': [
            'Colosseum', 'Vatican Museums', 'Trevi Fountain',
            'Pantheon', 'Roman Forum', 'Spanish Steps',
            'Sistine Chapel', 'Piazza Navona'
        ],
        'Tokyo': [
            'Senso-ji Temple', 'Tokyo Tower', 'Shibuya Crossing',
            'Meiji Shrine', 'Imperial Palace', 'Tsukiji Market',
            'Akihabara', 'Mount Fuji'
        ],
        'New York': [
            'Statue of Liberty', 'Central Park', 'Empire State Building',
            'Times Square', 'Brooklyn Bridge', 'Metropolitan Museum',
            'Broadway Show', '9/11 Memorial'
        ],
    }
    
    DEFAULT_ATTRACTIONS = [
        'City Center', 'Historic District', 'Local Market',
        'Main Square', 'Cultural Museum', 'Scenic Viewpoint',
        'Popular Restaurant', 'Shopping District'
    ]
    
    ACTIVITY_TYPES = {
        'morning': ['breakfast', 'walking tour', 'museum visit', 'market exploration'],
        'afternoon': ['lunch', 'sightseeing', 'shopping', 'local experience'],
        'evening': ['dinner', 'sunset viewing', 'entertainment', 'nightlife']
    }
    
    @classmethod
    def generate_itinerary(
        cls,
        destination: str,
        start_date,
        end_date,
        preferences: Dict = None
    ) -> List[Dict]:
        """
        Generate a daily itinerary for the trip.
        
        Args:
            destination: Destination city
            start_date: Trip start date
            end_date: Trip end date
            preferences: User preferences
            
        Returns:
            List of daily itinerary dictionaries
        """
        if preferences is None:
            preferences = {}
        
        # Convert to date objects if needed
        if hasattr(start_date, 'date'):
            start_date = start_date.date()
        if hasattr(end_date, 'date'):
            end_date = end_date.date()
        
        # Calculate number of days
        num_days = (end_date - start_date).days
        if num_days <= 0:
            num_days = 1
        
        # Get attractions for the destination
        attractions = cls.CITY_ATTRACTIONS.get(destination, cls.DEFAULT_ATTRACTIONS)
        
        itinerary_days = []
        
        for day_num in range(1, num_days + 1):
            current_date = start_date + timedelta(days=day_num - 1)
            
            # Generate title and description based on day
            if day_num == 1:
                title = f"Arrival and {destination} Introduction"
                description = f"Arrive in {destination}, check into hotel, and explore the neighborhood. Get oriented with the city and enjoy your first evening."
            elif day_num == num_days:
                title = f"Final Day in {destination}"
                description = f"Last-minute shopping, visit any missed attractions, and prepare for departure."
            else:
                # Pick a main attraction for the day
                if len(attractions) >= day_num - 1:
                    main_attraction = attractions[day_num - 1]
                else:
                    main_attraction = random.choice(attractions)
                title = f"Exploring {main_attraction}"
                description = f"Full day dedicated to visiting {main_attraction} and surrounding areas."
            
            # Generate activities for the day
            activities = cls._generate_activities(day_num, num_days, attractions, preferences)
            
            itinerary_day = {
                'day_number': day_num,
                'date': current_date,
                'title': title,
                'description': description,
                'activities': activities,
            }
            
            itinerary_days.append(itinerary_day)
        
        return itinerary_days
    
    @classmethod
    def _generate_activities(
        cls,
        day_num: int,
        total_days: int,
        attractions: List[str],
        preferences: Dict
    ) -> List[Dict]:
        """Generate activities for a specific day."""
        activities = []
        
        travel_style = preferences.get('travel_style', 'standard')
        
        # Morning activity
        if day_num == 1:
            activities.append({
                'time': '09:00',
                'activity': 'Arrive and check-in',
                'description': 'Check into your accommodation and freshen up',
                'duration': '2 hours'
            })
        else:
            morning_activity = random.choice(cls.ACTIVITY_TYPES['morning'])
            attraction = random.choice(attractions) if attractions else 'local area'
            activities.append({
                'time': '09:00',
                'activity': f'{morning_activity.title()} at {attraction}',
                'description': f'Start your day with a {morning_activity}',
                'duration': '2-3 hours'
            })
        
        # Afternoon activity
        afternoon_activity = random.choice(cls.ACTIVITY_TYPES['afternoon'])
        attraction = random.choice(attractions) if attractions else 'local area'
        activities.append({
            'time': '13:00',
            'activity': f'{afternoon_activity.title()} at {attraction}',
            'description': f'Spend your afternoon {afternoon_activity}',
            'duration': '3-4 hours'
        })
        
        # Evening activity
        if day_num == total_days:
            activities.append({
                'time': '19:00',
                'activity': 'Farewell dinner',
                'description': 'Enjoy a final meal and prepare for departure',
                'duration': '2 hours'
            })
        else:
            evening_activity = random.choice(cls.ACTIVITY_TYPES['evening'])
            activities.append({
                'time': '19:00',
                'activity': f'{evening_activity.title()}',
                'description': f'End your day with {evening_activity}',
                'duration': '2-3 hours'
            })
        
        return activities
