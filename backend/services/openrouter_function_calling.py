"""
OpenRouter LLM Function Calling Service with Amadeus SDK Integration

This service uses OpenRouter (with Claude Sonnet 4.5) to enable natural language
function calling for all Amadeus travel APIs. It maintains conversation context
and intelligently routes requests to appropriate Amadeus functions.
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional
import httpx

from .amadeus_service import AmadeusService

# Configure logging
logger = logging.getLogger(__name__)


# Common IATA codes for reference in system messages
COMMON_IATA_CODES = {
    'cities': 'PAR (Paris), LON (London), NYC (New York), ROM (Rome), BCN (Barcelona), BUH (Bucharest)',
    'airports': 'JFK, LAX, CDG, LHR, FCO, OTP (major airports)'
}


class OpenRouterFunctionCallingService:
    """
    Comprehensive LLM-powered function calling service using OpenRouter.
    Supports all Amadeus API functions with natural language understanding.
    Maintains conversation context across chat sessions.
    """
    
    def __init__(self, api_key: Optional[str] = None, timeout: int = 60):
        """
        Initialize the OpenRouter function calling service.
        
        Args:
            api_key: OpenRouter API key (defaults to env var OPENROUTER_API_KEY)
            timeout: Request timeout in seconds (default: 60)
        """
        self.api_key = api_key or os.getenv('OPENROUTER_API_KEY')
        if not self.api_key:
            raise ValueError("OpenRouter API key not provided. Set OPENROUTER_API_KEY environment variable.")
        
        self.model = "anthropic/claude-3.5-sonnet"
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.timeout = timeout
        self.amadeus = None  # Lazy initialization
        
    def _get_amadeus_service(self) -> AmadeusService:
        """Get or create Amadeus service instance."""
        if self.amadeus is None:
            self.amadeus = AmadeusService()
        return self.amadeus
    
    def get_function_definitions(self) -> List[Dict[str, Any]]:
        """
        Get all Amadeus API function definitions for LLM function calling.
        
        Returns:
            List of tool definitions compatible with OpenRouter/Claude
        """
        return [
            # ==================== FLIGHT FUNCTIONS ====================
            {
                "name": "search_flights",
                "description": "Search for flight offers between two cities/airports. Use this when the user wants to find flights, book a flight, or check flight availability. Supports one-way and round-trip searches.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "origin": {
                            "type": "string",
                            "description": "IATA code of origin airport (e.g., 'JFK', 'LAX', 'OTP')"
                        },
                        "destination": {
                            "type": "string",
                            "description": "IATA code of destination airport (e.g., 'CDG', 'LHR', 'BCN')"
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
                            "description": "Return date in YYYY-MM-DD format (for round trip, omit for one-way)"
                        },
                        "children": {
                            "type": "integer",
                            "description": "Number of children (2-11 years)",
                            "default": 0
                        },
                        "infants": {
                            "type": "integer",
                            "description": "Number of infants (under 2 years)",
                            "default": 0
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
                        },
                        "currency": {
                            "type": "string",
                            "description": "Currency code (e.g., 'USD', 'EUR', 'RON')",
                            "default": "USD"
                        },
                        "max_results": {
                            "type": "integer",
                            "description": "Maximum number of flight offers to return",
                            "default": 10
                        }
                    },
                    "required": ["origin", "destination", "departure_date"]
                }
            },
            {
                "name": "get_flight_cheapest_dates",
                "description": "Find the cheapest dates to fly between two locations. Use this when the user asks for the cheapest time to fly, best flight deals, or wants flexible dates.",
                "input_schema": {
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
            },
            {
                "name": "predict_flight_delay",
                "description": "Predict the likelihood of a flight being delayed. Use this when the user asks about potential delays or flight punctuality.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "origin": {
                            "type": "string",
                            "description": "Origin airport IATA code"
                        },
                        "destination": {
                            "type": "string",
                            "description": "Destination airport IATA code"
                        },
                        "departure_date": {
                            "type": "string",
                            "description": "Departure date in YYYY-MM-DD format"
                        },
                        "departure_time": {
                            "type": "string",
                            "description": "Departure time in HH:MM:SS format"
                        },
                        "arrival_date": {
                            "type": "string",
                            "description": "Arrival date in YYYY-MM-DD format"
                        },
                        "arrival_time": {
                            "type": "string",
                            "description": "Arrival time in HH:MM:SS format"
                        },
                        "airline_code": {
                            "type": "string",
                            "description": "2-character airline IATA code"
                        },
                        "flight_number": {
                            "type": "string",
                            "description": "Flight number"
                        }
                    },
                    "required": ["origin", "destination", "departure_date", "departure_time", "arrival_date", "arrival_time", "airline_code", "flight_number"]
                }
            },
            
            # ==================== HOTEL FUNCTIONS ====================
            {
                "name": "search_hotels_by_city",
                "description": "Search for hotel offers in a specific city. Use this when the user wants to find hotels, accommodation, or places to stay.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "city_code": {
                            "type": "string",
                            "description": "IATA city code (e.g., 'PAR' for Paris, 'LON' for London, 'NYC' for New York)"
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
                        },
                        "currency": {
                            "type": "string",
                            "description": "Currency code",
                            "default": "USD"
                        },
                        "radius": {
                            "type": "integer",
                            "description": "Search radius in kilometers",
                            "default": 5
                        },
                        "radius_unit": {
                            "type": "string",
                            "enum": ["KM", "MILE"],
                            "description": "Unit for search radius",
                            "default": "KM"
                        }
                    },
                    "required": ["city_code", "check_in_date", "check_out_date"]
                }
            },
            {
                "name": "get_hotel_ratings",
                "description": "Get sentiment analysis and ratings for hotels. Use this when the user asks about hotel quality, reviews, or ratings.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "hotel_ids": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of Amadeus hotel IDs (max 3)",
                            "maxItems": 3
                        }
                    },
                    "required": ["hotel_ids"]
                }
            },
            {
                "name": "search_hotel_by_name",
                "description": "Search for hotels by name (autocomplete). Use this when the user mentions a specific hotel name.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "keyword": {
                            "type": "string",
                            "description": "Hotel name or keyword to search for"
                        }
                    },
                    "required": ["keyword"]
                }
            },
            
            # ==================== ACTIVITIES & POI FUNCTIONS ====================
            {
                "name": "search_activities",
                "description": "Search for tours and activities at a specific location. Use this when the user asks what to do, activities available, or tours to book.",
                "input_schema": {
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
                            "default": 1,
                            "minimum": 1,
                            "maximum": 20
                        }
                    },
                    "required": ["latitude", "longitude"]
                }
            },
            {
                "name": "search_points_of_interest",
                "description": "Search for points of interest like landmarks, attractions, restaurants, and nightlife. Use this when the user asks about places to visit, things to see, or where to eat.",
                "input_schema": {
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
                            "items": {
                                "type": "string",
                                "enum": ["SIGHTS", "NIGHTLIFE", "RESTAURANT", "SHOPPING"]
                            },
                            "description": "POI categories to filter (e.g., ['SIGHTS', 'NIGHTLIFE', 'RESTAURANT'])"
                        }
                    },
                    "required": ["latitude", "longitude"]
                }
            },
            
            # ==================== LOCATION FUNCTIONS ====================
            {
                "name": "search_locations",
                "description": "Search for airports, cities, and locations by keyword. Use this when you need to find IATA codes, airport information, or city details. ALWAYS use this first when the user provides city/airport names instead of codes.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "keyword": {
                            "type": "string",
                            "description": "Search keyword (city name, airport name, etc.)"
                        },
                        "sub_type": {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "enum": ["AIRPORT", "CITY"]
                            },
                            "description": "Location types to filter (e.g., ['AIRPORT', 'CITY'])"
                        }
                    },
                    "required": ["keyword"]
                }
            },
            {
                "name": "search_airports",
                "description": "Search for nearest airports by coordinates. Use this when the user asks about nearby airports or airports near a specific location.",
                "input_schema": {
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
                            "default": 500
                        }
                    },
                    "required": ["latitude", "longitude"]
                }
            },
            
            # ==================== TRANSFER FUNCTIONS ====================
            {
                "name": "search_transfers",
                "description": "Search for ground transfers like taxis, shuttles, and private cars. Use this when the user asks about airport transfers, transportation, or rides.",
                "input_schema": {
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
            },
            
            # ==================== RECOMMENDATION FUNCTIONS ====================
            {
                "name": "get_travel_recommendations",
                "description": "Get AI-powered travel destination recommendations from an origin city. Use this when the user asks where they should travel, needs destination ideas, or wants recommendations.",
                "input_schema": {
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
            },
            
            # ==================== AIRLINE & AIRPORT INFO ====================
            {
                "name": "lookup_airline",
                "description": "Look up airline information by code. Use this when the user asks about an airline or wants to know what an airline code means.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "airline_code": {
                            "type": "string",
                            "description": "2-letter IATA airline code (e.g., 'AA', 'DL', 'LH', 'BA')"
                        }
                    },
                    "required": ["airline_code"]
                }
            },
            {
                "name": "get_airport_routes",
                "description": "Get all flight routes departing from an airport. Use this when the user asks where they can fly from an airport or what destinations are available.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "airport_code": {
                            "type": "string",
                            "description": "3-letter IATA airport code (e.g., 'JFK', 'LAX', 'CDG')"
                        },
                        "max_results": {
                            "type": "integer",
                            "description": "Maximum number of routes to return",
                            "default": 50
                        }
                    },
                    "required": ["airport_code"]
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
            'get_flight_cheapest_dates': amadeus.get_flight_cheapest_dates,
            'predict_flight_delay': amadeus.predict_flight_delay,
            'search_hotels_by_city': amadeus.search_hotels_by_city,
            'get_hotel_ratings': amadeus.get_hotel_ratings,
            'search_hotel_by_name': amadeus.search_hotel_by_name,
            'search_activities': amadeus.search_activities,
            'search_points_of_interest': amadeus.search_points_of_interest,
            'search_locations': amadeus.search_locations,
            'search_airports': amadeus.search_airports,
            'search_transfers': amadeus.search_transfers,
            'get_travel_recommendations': amadeus.get_travel_recommendations,
            'lookup_airline': amadeus.lookup_airline,
            'get_airport_routes': amadeus.get_airport_routes,
        }
        
        if function_name not in function_map:
            return {
                'success': False,
                'error': f'Unknown function: {function_name}'
            }
        
        try:
            # Execute the function with provided arguments
            logger.info(f"Executing {function_name} with arguments: {arguments}")
            result = function_map[function_name](**arguments)
            return result
        except Exception as e:
            logger.error(f"Error executing {function_name}: {str(e)}")
            return {
                'success': False,
                'error': f'Error executing {function_name}: {str(e)}'
            }
    
    def chat_with_function_calling(
        self,
        user_message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        max_iterations: int = 5
    ) -> Dict[str, Any]:
        """
        Process a user message with LLM function calling using OpenRouter.
        Maintains conversation context and makes intelligent function calls.
        
        Args:
            user_message: User's message in natural language
            conversation_history: Previous conversation messages for context
            max_iterations: Maximum number of function calling iterations
            
        Returns:
            Dictionary with:
                - response: Assistant's natural language response
                - function_calls: List of function calls made
                - conversation: Updated conversation history
                - success: Whether the operation was successful
        """
        # Build message history with context
        messages = conversation_history if conversation_history else []
        
        # System message to guide the LLM
        system_message = {
            "role": "system",
            "content": """You are a helpful and intelligent travel planning assistant with access to comprehensive Amadeus travel APIs.

Your capabilities include:
- Searching for flights (including cheapest dates and delay predictions)
- Finding hotels and accommodation
- Discovering activities and points of interest
- Providing travel recommendations
- Looking up airline and airport information
- Arranging ground transfers

Important guidelines:
1. When users provide city or airport names (not codes), ALWAYS use search_locations first to get the IATA codes
2. Be proactive in understanding user intent, even with vague requests
3. For queries about cheapest flights or flexible dates, use get_flight_cheapest_dates
4. Always provide helpful context and explanations with the data
5. If a function call fails, explain the issue and suggest alternatives
6. Maintain natural conversation flow

Common IATA codes:
- Cities: {cities}
- Airports: {airports}

Always be friendly, informative, and helpful in your responses.""".format(
                cities=COMMON_IATA_CODES['cities'],
                airports=COMMON_IATA_CODES['airports']
            )
        }
        
        # Prepare messages for API call
        api_messages = [system_message] + messages + [{"role": "user", "content": user_message}]
        
        function_calls_made = []
        iteration = 0
        
        try:
            while iteration < max_iterations:
                iteration += 1
                
                # Prepare request payload for OpenRouter
                payload = {
                    "model": self.model,
                    "messages": api_messages,
                    "tools": [
                        {
                            "type": "function",
                            "function": {
                                "name": tool["name"],
                                "description": tool["description"],
                                "parameters": tool["input_schema"]
                            }
                        }
                        for tool in self.get_function_definitions()
                    ]
                }
                
                # Make API call to OpenRouter
                with httpx.Client(timeout=self.timeout) as client:
                    response = client.post(
                        self.base_url,
                        headers={
                            "Authorization": f"Bearer {self.api_key}",
                            "Content-Type": "application/json"
                        },
                        json=payload
                    )
                    response.raise_for_status()
                    result = response.json()
                
                # Get the assistant's response
                assistant_message = result['choices'][0]['message']
                
                # Check if there are tool calls
                tool_calls = assistant_message.get('tool_calls', [])
                
                if not tool_calls:
                    # No more function calls, we have the final response
                    final_response = assistant_message.get('content', '')
                    break
                
                # Add assistant message to conversation
                api_messages.append(assistant_message)
                
                # Execute each tool call
                for tool_call in tool_calls:
                    function_name = tool_call['function']['name']
                    function_args = json.loads(tool_call['function']['arguments'])
                    
                    # Execute the function
                    function_result = self.execute_function(function_name, function_args)
                    
                    # Record the function call
                    function_calls_made.append({
                        'function': function_name,
                        'arguments': function_args,
                        'result': function_result
                    })
                    
                    # Add tool result to messages
                    api_messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call['id'],
                        "name": function_name,
                        "content": json.dumps(function_result)
                    })
                
                # Continue loop to get final response with function results
            else:
                # Max iterations reached
                final_response = "I apologize, but I've reached the maximum number of processing steps. Please try rephrasing your request."
            
            # Build the final conversation history (excluding system message)
            final_conversation = messages + [
                {"role": "user", "content": user_message},
                {"role": "assistant", "content": final_response}
            ]
            
            return {
                'success': True,
                'response': final_response,
                'function_calls': function_calls_made,
                'conversation': final_conversation
            }
            
        except httpx.HTTPStatusError as e:
            error_msg = f"OpenRouter API error: {e.response.status_code} - {e.response.text}"
            logger.error(error_msg)
            return {
                'success': False,
                'error': error_msg,
                'response': f"I apologize, but I encountered an error connecting to the AI service: {str(e)}",
                'function_calls': function_calls_made,
                'conversation': messages + [{"role": "user", "content": user_message}]
            }
        except Exception as e:
            error_msg = f"Error in chat processing: {str(e)}"
            logger.error(error_msg)
            return {
                'success': False,
                'error': error_msg,
                'response': f"I apologize, but I encountered an error: {str(e)}",
                'function_calls': function_calls_made,
                'conversation': messages + [{"role": "user", "content": user_message}]
            }
