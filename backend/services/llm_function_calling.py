"""
LLM Function Calling Service

This service integrates OpenAI's function calling capabilities with Amadeus APIs.
It allows the LLM to intelligently call Amadeus functions based on user requests.
"""

import os
import json
from typing import Dict, Any, List, Optional
from openai import OpenAI
from .amadeus_service import AmadeusService


class LLMFunctionCallingService:
    """
    Service that enables LLM-powered function calling for Amadeus APIs.
    Uses OpenAI's function calling feature to intelligently route user requests
    to appropriate Amadeus API functions.
    """
    
    def __init__(self, openai_api_key: Optional[str] = None):
        """
        Initialize the LLM function calling service.
        
        Args:
            openai_api_key: OpenAI API key (defaults to env var OPENAI_API_KEY)
        """
        self.api_key = openai_api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key not provided. Set OPENAI_API_KEY environment variable.")
        
        self.client = OpenAI(api_key=self.api_key)
        self.amadeus = None  # Lazy initialization
        
    def _get_amadeus_service(self) -> AmadeusService:
        """Get or create Amadeus service instance."""
        if self.amadeus is None:
            self.amadeus = AmadeusService()
        return self.amadeus
    
    def get_function_definitions(self) -> List[Dict[str, Any]]:
        """
        Get OpenAI function definitions for all Amadeus APIs.
        
        Returns:
            List of function definition dictionaries
        """
        return [
            {
                "type": "function",
                "function": {
                    "name": "search_flights",
                    "description": "Search for flight offers between two locations. Returns available flight options with prices, airlines, departure/arrival times.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "origin": {
                                "type": "string",
                                "description": "IATA code of origin airport (e.g., 'JFK', 'LAX')"
                            },
                            "destination": {
                                "type": "string",
                                "description": "IATA code of destination airport (e.g., 'CDG', 'LHR')"
                            },
                            "departure_date": {
                                "type": "string",
                                "description": "Departure date in YYYY-MM-DD format"
                            },
                            "adults": {
                                "type": "integer",
                                "description": "Number of adult travelers (12+ years)",
                                "default": 1
                            },
                            "return_date": {
                                "type": "string",
                                "description": "Return date in YYYY-MM-DD format (for round trip)"
                            },
                            "travel_class": {
                                "type": "string",
                                "enum": ["ECONOMY", "PREMIUM_ECONOMY", "BUSINESS", "FIRST"],
                                "description": "Travel class preference"
                            },
                            "non_stop": {
                                "type": "boolean",
                                "description": "Only return non-stop flights",
                                "default": False
                            }
                        },
                        "required": ["origin", "destination", "departure_date"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "search_hotels_by_city",
                    "description": "Search for hotel offers in a specific city. Returns available hotels with prices, ratings, amenities.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "city_code": {
                                "type": "string",
                                "description": "IATA city code (e.g., 'PAR' for Paris, 'LON' for London)"
                            },
                            "check_in_date": {
                                "type": "string",
                                "description": "Check-in date in YYYY-MM-DD format"
                            },
                            "check_out_date": {
                                "type": "string",
                                "description": "Check-out date in YYYY-MM-DD format"
                            },
                            "adults": {
                                "type": "integer",
                                "description": "Number of adult guests per room",
                                "default": 1
                            },
                            "room_quantity": {
                                "type": "integer",
                                "description": "Number of rooms",
                                "default": 1
                            }
                        },
                        "required": ["city_code", "check_in_date", "check_out_date"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "search_activities",
                    "description": "Search for tours and activities at a specific location. Returns available activities with descriptions, prices, and booking information.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "latitude": {
                                "type": "number",
                                "description": "Latitude coordinate of the location"
                            },
                            "longitude": {
                                "type": "number",
                                "description": "Longitude coordinate of the location"
                            },
                            "radius": {
                                "type": "integer",
                                "description": "Search radius in kilometers (1-20)",
                                "default": 1
                            }
                        },
                        "required": ["latitude", "longitude"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "search_points_of_interest",
                    "description": "Search for points of interest (landmarks, attractions, restaurants) at a location. Returns POIs with descriptions, ratings, and categories.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "latitude": {
                                "type": "number",
                                "description": "Latitude coordinate"
                            },
                            "longitude": {
                                "type": "number",
                                "description": "Longitude coordinate"
                            },
                            "radius": {
                                "type": "integer",
                                "description": "Search radius in kilometers",
                                "default": 1
                            },
                            "categories": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "POI categories to filter (e.g., ['SIGHTS', 'NIGHTLIFE', 'RESTAURANT'])"
                            }
                        },
                        "required": ["latitude", "longitude"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "search_locations",
                    "description": "Search for airports, cities, and locations by keyword. Useful for finding IATA codes or location details.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "keyword": {
                                "type": "string",
                                "description": "Search keyword (city name, airport name, etc.)"
                            },
                            "sub_type": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Location types to filter (e.g., ['AIRPORT', 'CITY'])"
                            }
                        },
                        "required": ["keyword"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_travel_recommendations",
                    "description": "Get AI-powered travel destination recommendations based on an origin city. Returns recommended destinations.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "origin": {
                                "type": "string",
                                "description": "Origin city IATA code"
                            },
                            "destination_country": {
                                "type": "string",
                                "description": "Optional destination country code (ISO 3166-1 alpha-2)"
                            },
                            "max_results": {
                                "type": "integer",
                                "description": "Maximum number of recommendations",
                                "default": 10
                            }
                        },
                        "required": ["origin"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "search_transfers",
                    "description": "Search for ground transfers (taxis, shuttles, private cars) between two locations.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "start_latitude": {
                                "type": "number",
                                "description": "Starting point latitude"
                            },
                            "start_longitude": {
                                "type": "number",
                                "description": "Starting point longitude"
                            },
                            "end_latitude": {
                                "type": "number",
                                "description": "Destination latitude"
                            },
                            "end_longitude": {
                                "type": "number",
                                "description": "Destination longitude"
                            },
                            "start_date_time": {
                                "type": "string",
                                "description": "Pickup date/time in ISO format (e.g., '2024-11-22T10:00:00')"
                            },
                            "passengers": {
                                "type": "integer",
                                "description": "Number of passengers",
                                "default": 1
                            }
                        },
                        "required": ["start_latitude", "start_longitude", "end_latitude", "end_longitude", "start_date_time"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_flight_cheapest_dates",
                    "description": "Find the cheapest dates to fly between two locations. Useful for flexible travel planning.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "origin": {
                                "type": "string",
                                "description": "IATA code of origin airport"
                            },
                            "destination": {
                                "type": "string",
                                "description": "IATA code of destination airport"
                            },
                            "departure_date": {
                                "type": "string",
                                "description": "Optional departure date to search around (YYYY-MM-DD)"
                            },
                            "one_way": {
                                "type": "boolean",
                                "description": "True for one-way, False for round-trip",
                                "default": False
                            }
                        },
                        "required": ["origin", "destination"]
                    }
                }
            }
        ]
    
    def execute_function(self, function_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute an Amadeus function based on the function name and arguments.
        
        Args:
            function_name: Name of the function to execute
            arguments: Dictionary of function arguments
            
        Returns:
            Dictionary with function execution result
        """
        amadeus = self._get_amadeus_service()
        
        # Map function names to Amadeus service methods
        function_map = {
            'search_flights': amadeus.search_flights,
            'search_hotels_by_city': amadeus.search_hotels_by_city,
            'search_activities': amadeus.search_activities,
            'search_points_of_interest': amadeus.search_points_of_interest,
            'search_locations': amadeus.search_locations,
            'get_travel_recommendations': amadeus.get_travel_recommendations,
            'search_transfers': amadeus.search_transfers,
            'get_flight_cheapest_dates': amadeus.get_flight_cheapest_dates,
        }
        
        if function_name not in function_map:
            return {
                'success': False,
                'error': f'Unknown function: {function_name}'
            }
        
        try:
            # Execute the function with provided arguments
            result = function_map[function_name](**arguments)
            return result
        except Exception as e:
            return {
                'success': False,
                'error': f'Error executing {function_name}: {str(e)}'
            }
    
    def chat_with_function_calling(
        self,
        user_message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        model: str = "gpt-4-turbo-preview"
    ) -> Dict[str, Any]:
        """
        Process a user message with LLM function calling.
        
        Args:
            user_message: User's message
            conversation_history: Previous conversation messages
            model: OpenAI model to use
            
        Returns:
            Dictionary with:
                - response: Assistant's response text
                - function_calls: List of function calls made
                - conversation: Updated conversation history
        """
        # Build message history
        messages = conversation_history if conversation_history else []
        messages.append({"role": "user", "content": user_message})
        
        # System message to guide the LLM
        system_message = {
            "role": "system",
            "content": """You are a helpful travel planning assistant with access to Amadeus travel APIs. 
            You can search for flights, hotels, activities, points of interest, and more.
            When users ask for travel information, use the available functions to get real data.
            Always provide helpful, accurate information and suggestions based on the function results.
            If you need location codes (like IATA codes), use the search_locations function first."""
        }
        
        messages.insert(0, system_message)
        
        function_calls_made = []
        
        try:
            # First API call with function definitions
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                tools=self.get_function_definitions(),
                tool_choice="auto"
            )
            
            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls
            
            # If the model wants to call functions
            if tool_calls:
                messages.append(response_message)
                
                # Execute each function call
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    
                    # Execute the function
                    function_result = self.execute_function(function_name, function_args)
                    
                    # Record the function call
                    function_calls_made.append({
                        'function': function_name,
                        'arguments': function_args,
                        'result': function_result
                    })
                    
                    # Add function result to messages
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": function_name,
                        "content": json.dumps(function_result)
                    })
                
                # Second API call to get the final response
                second_response = self.client.chat.completions.create(
                    model=model,
                    messages=messages
                )
                
                final_message = second_response.choices[0].message.content
            else:
                # No function calls needed
                final_message = response_message.content
            
            # Add assistant's response to conversation
            messages.append({"role": "assistant", "content": final_message})
            
            return {
                'success': True,
                'response': final_message,
                'function_calls': function_calls_made,
                'conversation': messages[1:]  # Exclude system message
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error in chat processing: {str(e)}',
                'response': f'I apologize, but I encountered an error: {str(e)}',
                'function_calls': function_calls_made,
                'conversation': messages[1:]
            }
