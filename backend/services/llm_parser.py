import re
from datetime import datetime, timedelta
from typing import Dict, Optional


class LLMParserService:
    """
    Service to parse user messages and extract trip details.
    This is a mock implementation - in production, this would use an actual LLM API.
    """
    
    @staticmethod
    def parse_message(message: str) -> Dict:
        """
        Parse user message and extract trip planning details.
        
        Args:
            message: User's trip planning message
            
        Returns:
            Dictionary containing extracted trip details
        """
        parsed_data = {
            'destination': None,
            'start_date': None,
            'end_date': None,
            'budget': None,
            'travelers_count': 1,
            'preferences': {}
        }
        
        message_lower = message.lower()
        
        # Extract destination (simple pattern matching with case-insensitive search)
        destination_patterns = [
            r'(?:to|in|visit)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)',  # Match 1-2 capitalized words
            r'trip\s+to\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)',
        ]
        
        for pattern in destination_patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                # Capitalize the destination and remove common non-destination words
                destination = match.group(1).strip()
                # Remove common trailing words
                for word in ['next', 'this', 'for', 'with', 'in']:
                    if destination.lower().endswith(' ' + word):
                        destination = destination[:-len(word)-1].strip()
                parsed_data['destination'] = destination.title()
                break
        
        # Extract dates
        # Look for patterns like "in January", "next week", "from X to Y"
        if 'next week' in message_lower:
            parsed_data['start_date'] = (datetime.now() + timedelta(days=7)).date()
            parsed_data['end_date'] = (datetime.now() + timedelta(days=10)).date()
        elif 'next month' in message_lower:
            parsed_data['start_date'] = (datetime.now() + timedelta(days=30)).date()
            parsed_data['end_date'] = (datetime.now() + timedelta(days=35)).date()
        else:
            # Default to 2 weeks from now
            parsed_data['start_date'] = (datetime.now() + timedelta(days=14)).date()
            parsed_data['end_date'] = (datetime.now() + timedelta(days=17)).date()
        
        # Extract budget
        budget_match = re.search(r'\$?(\d+(?:,\d{3})*(?:\.\d{2})?)', message)
        if budget_match:
            budget_str = budget_match.group(1).replace(',', '')
            try:
                parsed_data['budget'] = float(budget_str)
            except ValueError:
                pass
        
        # Extract number of travelers
        travelers_patterns = [
            r'(\d+)\s+(?:people|persons|travelers|guests)',
            r'for\s+(\d+)',
            r'(\d+)\s+of\s+us',
        ]
        
        for pattern in travelers_patterns:
            match = re.search(pattern, message_lower)
            if match:
                try:
                    parsed_data['travelers_count'] = int(match.group(1))
                    break
                except ValueError:
                    pass
        
        # Extract preferences
        preferences = {}
        
        if 'beach' in message_lower:
            preferences['type'] = 'beach'
        elif 'mountain' in message_lower or 'hiking' in message_lower:
            preferences['type'] = 'mountain'
        elif 'city' in message_lower or 'urban' in message_lower:
            preferences['type'] = 'city'
        
        if 'luxury' in message_lower or 'premium' in message_lower:
            preferences['accommodation_level'] = 'luxury'
        elif 'budget' in message_lower:
            preferences['accommodation_level'] = 'budget'
        
        if 'family' in message_lower:
            preferences['travel_style'] = 'family'
        elif 'romantic' in message_lower or 'honeymoon' in message_lower:
            preferences['travel_style'] = 'romantic'
        elif 'adventure' in message_lower:
            preferences['travel_style'] = 'adventure'
        
        parsed_data['preferences'] = preferences
        
        return parsed_data
