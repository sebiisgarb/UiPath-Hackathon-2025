"""
Chatbot Service with Tool-Calling Orchestration
Manages conversation history, state, and tool execution
"""

import json
import uuid
from typing import Dict, Any, List, Optional
from services.openrouter_service import OpenRouterService
from services.amadeus_tool_service import AmadeusToolService


class ChatbotService:
    """
    Main chatbot service for travel planning with LLM tool-calling.
    """
    
    def __init__(self):
        """Initialize chatbot service."""
        self.openrouter = OpenRouterService()
        self.amadeus = AmadeusToolService()
        
        # In-memory storage for sessions
        self.sessions = {}
    
    def get_or_create_session(self, session_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get or create a session.
        
        Args:
            session_id: Optional session identifier
            
        Returns:
            Session object with history and state
        """
        if session_id and session_id in self.sessions:
            return self.sessions[session_id]
        
        # Create new session
        new_id = session_id or str(uuid.uuid4())
        self.sessions[new_id] = {
            'id': new_id,
            'history': [],
            'state': {
                'origin_airport': None,
                'destination_airport': None,
                'departure_date': None,
                'return_date': None,
                'adults': None,
                'children': None,
            }
        }
        return self.sessions[new_id]
    
    def reset_session(self, session_id: str):
        """
        Reset a session.
        
        Args:
            session_id: Session identifier
        """
        if session_id in self.sessions:
            del self.sessions[session_id]
    
    def process_message(self, message: str, session_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Process a chat message with tool-calling orchestration.
        
        Args:
            message: User message
            session_id: Optional session identifier
            
        Returns:
            Response with reply, state, and history
        """
        session = self.get_or_create_session(session_id)
        
        # Add user message to history
        session['history'].append({
            'role': 'user',
            'content': message
        })
        
        # Prepare messages for OpenRouter
        messages = self._prepare_messages(session)
        
        # Get tools definition
        tools = self._get_tools_definition()
        
        # Tool execution loop
        max_iterations = 10
        iteration = 0
        
        while iteration < max_iterations:
            iteration += 1
            
            # Call OpenRouter
            response = self.openrouter.chat_completion(messages, tools, 'auto')
            assistant_message = self.openrouter.extract_message(response)
            
            # Check if there are tool calls
            if self.openrouter.has_tool_calls(assistant_message):
                # Add assistant message with tool calls to history
                session['history'].append({
                    'role': 'assistant',
                    'content': assistant_message.get('content') or '',
                    'tool_calls': assistant_message['tool_calls']
                })
                
                # Execute tool calls
                tool_results = self._execute_tool_calls(assistant_message['tool_calls'])
                
                # Add tool results to history
                for result in tool_results:
                    session['history'].append({
                        'role': 'tool',
                        'tool_call_id': result['tool_call_id'],
                        'name': result['name'],
                        'content': json.dumps(result['content'])
                    })
                
                # Update messages for next iteration
                messages = self._prepare_messages(session)
            else:
                # No tool calls, this is the final answer
                session['history'].append({
                    'role': 'assistant',
                    'content': assistant_message['content']
                })
                
                return {
                    'reply': assistant_message['content'],
                    'state': session['state'],
                    'history': session['history'],
                    'session_id': session['id']
                }
        
        # Max iterations reached
        final_message = "I apologize, but I'm having trouble completing this request. Please try rephrasing your question."
        session['history'].append({
            'role': 'assistant',
            'content': final_message
        })
        
        return {
            'reply': final_message,
            'state': session['state'],
            'history': session['history'],
            'session_id': session['id']
        }
    
    def _prepare_messages(self, session: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Prepare messages for OpenRouter with system message.
        
        Args:
            session: Session object
            
        Returns:
            List of messages
        """
        state = session['state']
        system_message = {
            'role': 'system',
            'content': f"""You are a helpful travel planning assistant with access to real-time flight, hotel, and activity data through the Amadeus API.

Your goal is to help users plan their trips by:
1. Understanding their travel preferences (origin, destination, dates, number of travelers)
2. Searching for flights, hotels, and activities using the available tools
3. Providing comprehensive travel recommendations

Current conversation state:
- Origin Airport: {state.get('origin_airport') or 'not set'}
- Destination Airport: {state.get('destination_airport') or 'not set'}
- Departure Date: {state.get('departure_date') or 'not set'}
- Return Date: {state.get('return_date') or 'not set'}
- Adults: {state.get('adults') or 'not set'}
- Children: {state.get('children') or 'not set'}

When you need information like flights or hotels, use the appropriate tools. Always be helpful and provide detailed, accurate information based on the API results.

Important: Extract and remember travel details from the conversation to update the state."""
        }
        
        return [system_message] + session['history']
    
    def _execute_tool_calls(self, tool_calls: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Execute tool calls from the LLM.
        
        Args:
            tool_calls: List of tool call objects
            
        Returns:
            List of tool results
        """
        results = []
        
        for tool_call in tool_calls:
            tool_id = tool_call['id']
            function_name = tool_call['function']['name']
            
            # Parse arguments
            try:
                arguments = json.loads(tool_call['function']['arguments'])
            except json.JSONDecodeError:
                results.append({
                    'tool_call_id': tool_id,
                    'name': function_name,
                    'content': {'error': 'Invalid arguments format'}
                })
                continue
            
            # Execute the tool
            try:
                result = self._call_amadeus_tool(function_name, arguments)
                results.append({
                    'tool_call_id': tool_id,
                    'name': function_name,
                    'content': result
                })
            except Exception as e:
                results.append({
                    'tool_call_id': tool_id,
                    'name': function_name,
                    'content': {'error': str(e)}
                })
        
        return results
    
    def _call_amadeus_tool(self, function_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call the appropriate Amadeus tool function.
        
        Args:
            function_name: Name of the function to call
            arguments: Function arguments
            
        Returns:
            Function result
        """
        # Map function names to Amadeus service methods
        if function_name == 'airport_city_search':
            return self.amadeus.airport_city_search(**arguments)
        elif function_name == 'flight_offers_search':
            return self.amadeus.flight_offers_search(**arguments)
        elif function_name == 'flight_inspiration_search':
            return self.amadeus.flight_inspiration_search(**arguments)
        elif function_name == 'flight_cheapest_date_search':
            return self.amadeus.flight_cheapest_date_search(**arguments)
        elif function_name == 'flight_offers_price':
            return self.amadeus.flight_offers_price(**arguments)
        elif function_name == 'airport_direct_destinations':
            return self.amadeus.airport_direct_destinations(**arguments)
        elif function_name == 'airline_destinations':
            return self.amadeus.airline_destinations(**arguments)
        elif function_name == 'hotel_list':
            return self.amadeus.hotel_list(**arguments)
        elif function_name == 'hotel_search':
            return self.amadeus.hotel_search(**arguments)
        elif function_name == 'hotel_offers_by_hotel':
            return self.amadeus.hotel_offers_by_hotel(**arguments)
        elif function_name == 'hotel_ratings':
            return self.amadeus.hotel_ratings(**arguments)
        elif function_name == 'tours_and_activities':
            return self.amadeus.tours_and_activities(**arguments)
        elif function_name == 'tours_and_activities_by_square':
            return self.amadeus.tours_and_activities_by_square(**arguments)
        elif function_name == 'get_activity_details':
            return self.amadeus.get_activity_details(**arguments)
        elif function_name == 'trip_purpose_prediction':
            return self.amadeus.trip_purpose_prediction(**arguments)
        else:
            raise ValueError(f"Unknown function: {function_name}")
    
    def _get_tools_definition(self) -> List[Dict[str, Any]]:
        """
        Get tools definition for OpenRouter in OpenAI function-calling format.
        
        Returns:
            List of tool definitions
        """
        return [
            {
                'type': 'function',
                'function': {
                    'name': 'airport_city_search',
                    'description': 'Search for airports and cities by keyword. Use this to find airport codes.',
                    'parameters': {
                        'type': 'object',
                        'properties': {
                            'keyword': {
                                'type': 'string',
                                'description': 'Search keyword (city name, airport name, etc.)'
                            },
                            'subType': {
                                'type': 'string',
                                'description': 'Optional: Filter by type (AIRPORT, CITY)',
                                'enum': ['AIRPORT', 'CITY']
                            }
                        },
                        'required': ['keyword']
                    }
                }
            },
            {
                'type': 'function',
                'function': {
                    'name': 'flight_offers_search',
                    'description': 'Search for flight offers between two locations.',
                    'parameters': {
                        'type': 'object',
                        'properties': {
                            'originLocationCode': {
                                'type': 'string',
                                'description': 'Origin airport IATA code (e.g., JFK)'
                            },
                            'destinationLocationCode': {
                                'type': 'string',
                                'description': 'Destination airport IATA code (e.g., LAX)'
                            },
                            'departureDate': {
                                'type': 'string',
                                'description': 'Departure date in YYYY-MM-DD format'
                            },
                            'adults': {
                                'type': 'integer',
                                'description': 'Number of adult travelers'
                            },
                            'returnDate': {
                                'type': 'string',
                                'description': 'Optional: Return date in YYYY-MM-DD format'
                            },
                            'children': {
                                'type': 'integer',
                                'description': 'Optional: Number of children'
                            },
                            'travelClass': {
                                'type': 'string',
                                'description': 'Optional: Travel class',
                                'enum': ['ECONOMY', 'PREMIUM_ECONOMY', 'BUSINESS', 'FIRST']
                            }
                        },
                        'required': ['originLocationCode', 'destinationLocationCode', 'departureDate', 'adults']
                    }
                }
            },
            {
                'type': 'function',
                'function': {
                    'name': 'flight_inspiration_search',
                    'description': 'Get inspirational flight destinations from an origin.',
                    'parameters': {
                        'type': 'object',
                        'properties': {
                            'origin': {
                                'type': 'string',
                                'description': 'Origin airport IATA code'
                            }
                        },
                        'required': ['origin']
                    }
                }
            },
            {
                'type': 'function',
                'function': {
                    'name': 'flight_cheapest_date_search',
                    'description': 'Find the cheapest dates to fly between two locations.',
                    'parameters': {
                        'type': 'object',
                        'properties': {
                            'origin': {
                                'type': 'string',
                                'description': 'Origin airport IATA code'
                            },
                            'destination': {
                                'type': 'string',
                                'description': 'Destination airport IATA code'
                            }
                        },
                        'required': ['origin', 'destination']
                    }
                }
            },
            {
                'type': 'function',
                'function': {
                    'name': 'flight_offers_price',
                    'description': 'Get confirmed pricing for a specific flight offer.',
                    'parameters': {
                        'type': 'object',
                        'properties': {
                            'flight_offer': {
                                'type': 'object',
                                'description': 'Flight offer object from flight_offers_search'
                            },
                            'include': {
                                'type': 'string',
                                'description': 'Optional fields to include in response'
                            }
                        },
                        'required': ['flight_offer']
                    }
                }
            },
            {
                'type': 'function',
                'function': {
                    'name': 'airport_direct_destinations',
                    'description': 'Get all direct destinations from a departure airport.',
                    'parameters': {
                        'type': 'object',
                        'properties': {
                            'departureAirportCode': {
                                'type': 'string',
                                'description': 'Departure airport IATA code'
                            }
                        },
                        'required': ['departureAirportCode']
                    }
                }
            },
            {
                'type': 'function',
                'function': {
                    'name': 'airline_destinations',
                    'description': 'Get all destinations served by an airline.',
                    'parameters': {
                        'type': 'object',
                        'properties': {
                            'airlineCode': {
                                'type': 'string',
                                'description': 'Airline IATA code (e.g., AA)'
                            }
                        },
                        'required': ['airlineCode']
                    }
                }
            },
            {
                'type': 'function',
                'function': {
                    'name': 'hotel_list',
                    'description': 'Get list of hotels in a city.',
                    'parameters': {
                        'type': 'object',
                        'properties': {
                            'cityCode': {
                                'type': 'string',
                                'description': 'IATA city code (e.g., PAR for Paris)'
                            }
                        },
                        'required': ['cityCode']
                    }
                }
            },
            {
                'type': 'function',
                'function': {
                    'name': 'hotel_search',
                    'description': 'Search for hotel offers.',
                    'parameters': {
                        'type': 'object',
                        'properties': {
                            'hotelIds': {
                                'type': 'array',
                                'items': {'type': 'string'},
                                'description': 'Array of hotel IDs'
                            },
                            'checkInDate': {
                                'type': 'string',
                                'description': 'Check-in date in YYYY-MM-DD format'
                            },
                            'checkOutDate': {
                                'type': 'string',
                                'description': 'Check-out date in YYYY-MM-DD format'
                            },
                            'adults': {
                                'type': 'integer',
                                'description': 'Number of adults'
                            }
                        },
                        'required': ['hotelIds', 'checkInDate', 'checkOutDate', 'adults']
                    }
                }
            },
            {
                'type': 'function',
                'function': {
                    'name': 'hotel_offers_by_hotel',
                    'description': 'Get offers for a specific hotel.',
                    'parameters': {
                        'type': 'object',
                        'properties': {
                            'hotelId': {
                                'type': 'string',
                                'description': 'Hotel ID'
                            }
                        },
                        'required': ['hotelId']
                    }
                }
            },
            {
                'type': 'function',
                'function': {
                    'name': 'hotel_ratings',
                    'description': 'Get hotel ratings and sentiment analysis.',
                    'parameters': {
                        'type': 'object',
                        'properties': {
                            'hotelIds': {
                                'type': 'array',
                                'items': {'type': 'string'},
                                'description': 'Array of hotel IDs (max 3)'
                            }
                        },
                        'required': ['hotelIds']
                    }
                }
            },
            {
                'type': 'function',
                'function': {
                    'name': 'tours_and_activities',
                    'description': 'Search for tours and activities by coordinates.',
                    'parameters': {
                        'type': 'object',
                        'properties': {
                            'latitude': {
                                'type': 'number',
                                'description': 'Latitude coordinate'
                            },
                            'longitude': {
                                'type': 'number',
                                'description': 'Longitude coordinate'
                            },
                            'radius': {
                                'type': 'number',
                                'description': 'Search radius in km (default: 1)'
                            }
                        },
                        'required': ['latitude', 'longitude']
                    }
                }
            },
            {
                'type': 'function',
                'function': {
                    'name': 'tours_and_activities_by_square',
                    'description': 'Search for tours and activities by bounding box.',
                    'parameters': {
                        'type': 'object',
                        'properties': {
                            'north': {'type': 'number', 'description': 'North boundary'},
                            'west': {'type': 'number', 'description': 'West boundary'},
                            'south': {'type': 'number', 'description': 'South boundary'},
                            'east': {'type': 'number', 'description': 'East boundary'}
                        },
                        'required': ['north', 'west', 'south', 'east']
                    }
                }
            },
            {
                'type': 'function',
                'function': {
                    'name': 'get_activity_details',
                    'description': 'Get details of a specific activity.',
                    'parameters': {
                        'type': 'object',
                        'properties': {
                            'activityId': {
                                'type': 'string',
                                'description': 'Activity ID'
                            }
                        },
                        'required': ['activityId']
                    }
                }
            },
            {
                'type': 'function',
                'function': {
                    'name': 'trip_purpose_prediction',
                    'description': 'Predict the purpose of a trip (business or leisure).',
                    'parameters': {
                        'type': 'object',
                        'properties': {
                            'originLocationCode': {
                                'type': 'string',
                                'description': 'Origin airport IATA code'
                            },
                            'destinationLocationCode': {
                                'type': 'string',
                                'description': 'Destination airport IATA code'
                            },
                            'departureDate': {
                                'type': 'string',
                                'description': 'Departure date in YYYY-MM-DD format'
                            },
                            'returnDate': {
                                'type': 'string',
                                'description': 'Return date in YYYY-MM-DD format'
                            }
                        },
                        'required': ['originLocationCode', 'destinationLocationCode', 'departureDate', 'returnDate']
                    }
                }
            }
        ]
