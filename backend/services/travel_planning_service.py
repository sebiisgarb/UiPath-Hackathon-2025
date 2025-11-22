"""
Travel Planning Service with Claude Sonnet 4.5 via OpenRouter

This service uses Claude Sonnet 4.5 through OpenRouter to extract travel information
from natural language and guide users through a structured workflow:
1. Destination
2. Travel Dates
3. Flight Selection
4. Hotel Selection
"""

import os
import json
import re
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import httpx


class TravelPlanningService:
    """
    Service for extracting and validating travel information from natural language.
    Uses Claude Sonnet 4.5 via OpenRouter for intelligent extraction.
    """
    
    # Workflow steps in order
    WORKFLOW_STEPS = ['destination', 'travel_dates', 'flight', 'hotel']
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the travel planning service.
        
        Args:
            api_key: OpenRouter API key (defaults to env var OPENROUTER_API_KEY)
        """
        self.api_key = api_key or os.getenv('OPENROUTER_API_KEY')
        if not self.api_key:
            raise ValueError("OpenRouter API key not provided. Set OPENROUTER_API_KEY environment variable.")
        
        self.model = "anthropic/claude-3.5-sonnet"
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
    
    def extract_travel_info(self, message: str, current_state: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Extract travel information from a natural language message.
        
        Args:
            message: User's message
            current_state: Current state of collected information
            
        Returns:
            Dictionary with:
                - extracted_info: Newly extracted information
                - collected_info: All collected information so far
                - next_question: Next question to ask the user
                - workflow_status: Status of each workflow step
                - is_complete: Whether all information is collected
        """
        if current_state is None:
            current_state = {
                'destination': None,
                'travel_dates': None,
                'flight': None,
                'hotel': None
            }
        
        # Use Claude to extract information from the message
        extracted = self._extract_with_claude(message, current_state)
        
        # Update current state with extracted information
        updated_state = current_state.copy()
        for key in self.WORKFLOW_STEPS:
            if extracted.get(key) and not updated_state.get(key):
                updated_state[key] = extracted[key]
        
        # Determine workflow status
        workflow_status = {
            'destination': {
                'completed': bool(updated_state.get('destination')),
                'data': updated_state.get('destination')
            },
            'travel_dates': {
                'completed': bool(updated_state.get('travel_dates')),
                'data': updated_state.get('travel_dates')
            },
            'flight': {
                'completed': bool(updated_state.get('flight')),
                'data': updated_state.get('flight')
            },
            'hotel': {
                'completed': bool(updated_state.get('hotel')),
                'data': updated_state.get('hotel')
            }
        }
        
        # Find the next incomplete step
        next_step = None
        for step in self.WORKFLOW_STEPS:
            if not workflow_status[step]['completed']:
                next_step = step
                break
        
        # Generate next question
        next_question = self._generate_next_question(next_step, updated_state)
        
        # Check if workflow is complete
        is_complete = all(workflow_status[step]['completed'] for step in self.WORKFLOW_STEPS)
        
        return {
            'extracted_info': extracted,
            'collected_info': updated_state,
            'next_question': next_question,
            'workflow_status': workflow_status,
            'is_complete': is_complete,
            'current_step': next_step
        }
    
    def _extract_with_claude(self, message: str, current_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Use Claude Sonnet to extract travel information from natural language.
        
        Args:
            message: User's message
            current_state: Current state of collected information
            
        Returns:
            Dictionary with extracted information
        """
        # Create a prompt for Claude to extract structured information
        system_prompt = """You are a travel information extraction assistant. Extract travel information from the user's message.

Return ONLY a JSON object with the following structure (include only fields that you can extract from the message):
{
    "destination": {
        "city": "city name",
        "country": "country name",
        "airport_code": "IATA code if mentioned"
    },
    "travel_dates": {
        "departure_date": "YYYY-MM-DD",
        "return_date": "YYYY-MM-DD",
        "duration_days": number
    },
    "flight": {
        "airline": "airline name if mentioned",
        "class": "economy/business/first if mentioned",
        "preferences": "any flight preferences"
    },
    "hotel": {
        "name": "hotel name if mentioned",
        "star_rating": number,
        "preferences": "any hotel preferences"
    }
}

Rules:
- Only include fields you can confidently extract from the message
- For dates, parse relative terms like "next week", "in December", etc.
- If information is already collected (shown below), don't extract it again unless user is changing it
- Return ONLY the JSON object, no other text

Already collected information:
""" + json.dumps(current_state, indent=2)
        
        user_prompt = f"Extract travel information from this message: {message}"
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.3,
                "max_tokens": 1000
            }
            
            with httpx.Client(timeout=30.0) as client:
                response = client.post(self.base_url, headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()
            
            # Extract the response content
            content = data['choices'][0]['message']['content']
            
            # Parse JSON from the response
            # Try to find JSON in the response
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                extracted = json.loads(json_match.group())
                return extracted
            else:
                return {}
                
        except Exception as e:
            print(f"Error extracting with Claude: {e}")
            # Fallback to simple extraction
            return self._fallback_extraction(message, current_state)
    
    def _fallback_extraction(self, message: str, current_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fallback extraction using simple pattern matching.
        """
        extracted = {}
        message_lower = message.lower()
        
        # Extract destination
        if not current_state.get('destination'):
            destination_patterns = [
                r'(?:to|visit|going to|destination)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)',
                r'in\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)',
            ]
            for pattern in destination_patterns:
                match = re.search(pattern, message, re.IGNORECASE)
                if match:
                    city = match.group(1).strip().title()
                    extracted['destination'] = {'city': city}
                    break
        
        # Extract dates
        if not current_state.get('travel_dates'):
            if 'next week' in message_lower:
                departure = datetime.now() + timedelta(days=7)
                return_date = departure + timedelta(days=7)
                extracted['travel_dates'] = {
                    'departure_date': departure.strftime('%Y-%m-%d'),
                    'return_date': return_date.strftime('%Y-%m-%d'),
                    'duration_days': 7
                }
            elif 'next month' in message_lower:
                departure = datetime.now() + timedelta(days=30)
                return_date = departure + timedelta(days=7)
                extracted['travel_dates'] = {
                    'departure_date': departure.strftime('%Y-%m-%d'),
                    'return_date': return_date.strftime('%Y-%m-%d'),
                    'duration_days': 7
                }
        
        # Extract flight preferences
        if not current_state.get('flight'):
            flight_info = {}
            if 'business class' in message_lower or 'business' in message_lower:
                flight_info['class'] = 'business'
            elif 'first class' in message_lower:
                flight_info['class'] = 'first'
            elif 'economy' in message_lower:
                flight_info['class'] = 'economy'
            
            if flight_info:
                extracted['flight'] = flight_info
        
        # Extract hotel preferences
        if not current_state.get('hotel'):
            hotel_info = {}
            if 'luxury' in message_lower or '5 star' in message_lower:
                hotel_info['star_rating'] = 5
            elif '4 star' in message_lower:
                hotel_info['star_rating'] = 4
            elif '3 star' in message_lower:
                hotel_info['star_rating'] = 3
            
            if hotel_info:
                extracted['hotel'] = hotel_info
        
        return extracted
    
    def _generate_next_question(self, next_step: Optional[str], current_state: Dict[str, Any]) -> str:
        """
        Generate the next question to ask the user based on the workflow.
        
        Args:
            next_step: The next step that needs information
            current_state: Current collected information
            
        Returns:
            Question to ask the user
        """
        if next_step is None:
            # All information collected
            summary = self._generate_summary(current_state)
            return f"Perfect! I have all the information I need:\n\n{summary}\n\nWould you like me to search for flights and hotels now?"
        
        questions = {
            'destination': "Where would you like to travel? Please tell me your destination city.",
            'travel_dates': f"Great! You're going to {current_state.get('destination', {}).get('city', 'your destination')}. When would you like to travel? Please provide your departure and return dates.",
            'flight': f"Excellent! Now let's find you a flight. Do you have any preferences for your flight (e.g., airline, class, direct flight)?",
            'hotel': f"Almost done! Do you have any preferences for your hotel (e.g., star rating, specific hotel name, location)?",
        }
        
        return questions.get(next_step, "What would you like to do?")
    
    def _generate_summary(self, state: Dict[str, Any]) -> str:
        """Generate a summary of collected information."""
        lines = []
        
        if state.get('destination'):
            dest = state['destination']
            lines.append(f"✓ Destination: {dest.get('city', 'Unknown')}")
        
        if state.get('travel_dates'):
            dates = state['travel_dates']
            lines.append(f"✓ Travel Dates: {dates.get('departure_date')} to {dates.get('return_date')} ({dates.get('duration_days')} days)")
        
        if state.get('flight'):
            flight = state['flight']
            prefs = []
            if flight.get('class'):
                prefs.append(f"{flight['class']} class")
            if flight.get('airline'):
                prefs.append(flight['airline'])
            if flight.get('preferences'):
                prefs.append(flight['preferences'])
            lines.append(f"✓ Flight: {', '.join(prefs) if prefs else 'Any'}")
        
        if state.get('hotel'):
            hotel = state['hotel']
            prefs = []
            if hotel.get('star_rating'):
                prefs.append(f"{hotel['star_rating']}-star")
            if hotel.get('name'):
                prefs.append(hotel['name'])
            if hotel.get('preferences'):
                prefs.append(hotel['preferences'])
            lines.append(f"✓ Hotel: {', '.join(prefs) if prefs else 'Any'}")
        
        return '\n'.join(lines)
    
    def format_response_for_frontend(self, result: Dict[str, Any], user_message: str) -> Dict[str, Any]:
        """
        Format the response in a frontend-friendly structure.
        
        Args:
            result: Result from extract_travel_info
            user_message: Original user message
            
        Returns:
            Dictionary with structured response for frontend
        """
        return {
            'success': True,
            'message': result['next_question'],
            'workflow': {
                'current_step': result.get('current_step'),
                'is_complete': result['is_complete'],
                'progress': {
                    'destination': {
                        'completed': result['workflow_status']['destination']['completed'],
                        'label': 'Destination',
                        'data': result['workflow_status']['destination']['data']
                    },
                    'travel_dates': {
                        'completed': result['workflow_status']['travel_dates']['completed'],
                        'label': 'Travel Dates',
                        'data': result['workflow_status']['travel_dates']['data']
                    },
                    'flight': {
                        'completed': result['workflow_status']['flight']['completed'],
                        'label': 'Flight Preferences',
                        'data': result['workflow_status']['flight']['data']
                    },
                    'hotel': {
                        'completed': result['workflow_status']['hotel']['completed'],
                        'label': 'Hotel Preferences',
                        'data': result['workflow_status']['hotel']['data']
                    }
                }
            },
            'collected_info': result['collected_info'],
            'extracted_from_message': result['extracted_info']
        }
