"""
Chatbot Service with Tool-Calling Orchestration
Manages conversation history, state, and tool execution
"""

import json
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from services.openrouter_service import OpenRouterService
from services.amadeus_tool_service import AmadeusToolService
from apps.chat.models import ChatSession


class ChatbotService:
    """
    Main chatbot service for travel planning with LLM tool-calling.
    """
    
    def __init__(self):
        """Initialize chatbot service."""
        self.openrouter = OpenRouterService()
        self.amadeus = AmadeusToolService()
        
        # In-memory sessions (ephemeral). For persistence consider Redis later.
        self.sessions: Dict[str, Dict[str, Any]] = {}
    
    def get_or_create_session(self, session_id: Optional[str] = None) -> Dict[str, Any]:
        """Return existing or new session dict, persisting state in DB."""
        if session_id and session_id in self.sessions:
            return self.sessions[session_id]
        new_id = session_id or str(uuid.uuid4())
        db_session = ChatSession.objects.filter(session_id=new_id).first()
        if not db_session:
            db_session = ChatSession.objects.create(
                session_id=new_id,
                workflow_state={
                    'origin_airport': None,
                    'destination_airport': None,
                    'departure_date': None,
                    'return_date': None,
                    'adults': None,
                    'children': None,
                    'flight_selection': None,
                    'hotel_selection': None,
                    'activities_selection': [],
                    'itinerary': None,
                    'progress_stage': 'initial'
                }
            )
        session = {
            'id': new_id,
            'history': [],  # messages remain ephemeral
            'state': db_session.workflow_state or {}
        }
        self.sessions[new_id] = session
        return session
    
    def reset_session(self, session_id: str):
        """Remove in-memory session and clear persistent workflow state."""
        ChatSession.objects.filter(session_id=session_id).delete()
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
        
        # Add user message with timestamp
        session['history'].append({'role': 'user', 'content': message, 'created_at': self._now()})
        
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
                    'content': assistant_message['content'],
                    'created_at': self._now()
                })
                return self._build_response(session)
        
        # Max iterations reached
        final_message = "I apologize, but I'm having trouble completing this request. Please try rephrasing your question."
        session['history'].append({
            'role': 'assistant',
            'content': final_message,
            'created_at': self._now()
        })
        return self._build_response(session, final_message)

    def _build_response(self, session: Dict[str, Any], reply_override: Optional[str] = None) -> Dict[str, Any]:
        history = session['history']
        self._persist_state(session)
        return {
            'reply': reply_override or (history[-1]['content'] if history else ''),
            'state': session['state'],
            'history': history,
            'session_id': session['id']
        }

    def _now(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def get_session_data(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Public accessor to build a response for an existing session id."""
        session = self.sessions.get(session_id)
        if not session:
            db_session = ChatSession.objects.filter(session_id=session_id).first()
            if not db_session:
                return None
            self.sessions[session_id] = {
                'id': session_id,
                'history': [],
                'state': db_session.workflow_state or {}
            }
            session = self.sessions[session_id]
        return self._build_response(session)

    def _persist_state(self, session: Dict[str, Any]):
        ChatSession.objects.filter(session_id=session['id']).update(workflow_state=session['state'])

    def update_state(self, session_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        session = self.sessions.get(session_id)
        if not session:
            return None
        session['state'].update(updates)
        self._persist_state(session)
        return session['state']
    
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
            'content': f"""Ești un asistent prietenos pentru planificarea călătoriilor, cu acces la date în timp real despre zboruri, hoteluri și activități prin API-ul Amadeus.

Obiectivul tău este să ajuți utilizatorii să-și planifice călătoriile prin:
1. Înțelegerea preferințelor lor de călătorie (origine, destinație, date, număr de călători)
2. Căutarea de zboruri, hoteluri și activități folosind instrumentele disponibile
3. Oferirea de recomandări complete de călătorie

Starea conversației curente:
- Aeroport de origine: {state.get('origin_airport') or 'nesetat'}
- Aeroport de destinație: {state.get('destination_airport') or 'nesetat'}
- Data plecării: {state.get('departure_date') or 'nesetat'}
- Data întoarcerii: {state.get('return_date') or 'nesetat'}
- Adulți: {state.get('adults') or 'nesetat'}
- Copii: {state.get('children') or 'nesetat'}

Când ai nevoie de informații precum zboruri sau hoteluri, folosește instrumentele corespunzătoare. Fii întotdeauna de ajutor și oferă informații detaliate și precise bazate pe rezultatele API-ului.

Important: Extrage și ține minte detaliile călătoriei din conversație pentru a actualiza starea. Răspunde ÎNTOTDEAUNA în limba română."""
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
