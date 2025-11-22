"""
Amadeus API Integration - Usage Examples

This file demonstrates how to use the Amadeus functions with the LLM function calling service.
"""

# Example 1: Using Amadeus Service Directly
# ==========================================

from services.amadeus_service import AmadeusService

# Initialize the service (reads credentials from environment variables)
amadeus = AmadeusService()

# Search for flights
print("Example 1: Search flights from JFK to CDG")
flight_result = amadeus.search_flights(
    origin='JFK',
    destination='CDG',
    departure_date='2025-12-01',
    adults=2,
    return_date='2025-12-15',
    travel_class='ECONOMY'
)

if flight_result['success']:
    print(f"Found {len(flight_result['data'])} flight options")
    # Process flight data
else:
    print(f"Error: {flight_result['error']}")


# Search for hotels
print("\nExample 2: Search hotels in Paris")
hotel_result = amadeus.search_hotels_by_city(
    city_code='PAR',
    check_in_date='2025-12-01',
    check_out_date='2025-12-05',
    adults=2,
    room_quantity=1
)

if hotel_result['success']:
    print(f"Found {len(hotel_result['data'])} hotel options")
else:
    print(f"Error: {hotel_result['error']}")


# Search for activities
print("\nExample 3: Search activities in Paris")
activities_result = amadeus.search_activities(
    latitude=48.8566,  # Paris coordinates
    longitude=2.3522,
    radius=5
)

if activities_result['success']:
    print(f"Found {len(activities_result['data'])} activities")
else:
    print(f"Error: {activities_result['error']}")


# Example 2: Using LLM Function Calling Service
# ==============================================

from services.llm_function_calling import LLMFunctionCallingService

# Initialize the LLM service
llm_service = LLMFunctionCallingService()

# Natural language query
print("\nExample 4: Natural language flight search")
result = llm_service.chat_with_function_calling(
    user_message="I want to fly from New York to Paris on December 1st, returning December 15th. Show me business class options for 2 adults."
)

if result['success']:
    print("Assistant response:")
    print(result['response'])
    print(f"\nFunction calls made: {len(result['function_calls'])}")
    for call in result['function_calls']:
        print(f"  - {call['function']} with args: {call['arguments']}")
else:
    print(f"Error: {result['error']}")


# Example 3: Multi-turn conversation
# ===================================

print("\nExample 5: Multi-turn conversation")

# First message
result1 = llm_service.chat_with_function_calling(
    user_message="I'm planning a trip to Paris"
)
print("User: I'm planning a trip to Paris")
print(f"Assistant: {result1['response']}")

# Continue conversation
result2 = llm_service.chat_with_function_calling(
    user_message="I want to go in December for 5 days. Find me flights from New York.",
    conversation_history=result1['conversation']
)
print("\nUser: I want to go in December for 5 days. Find me flights from New York.")
print(f"Assistant: {result2['response']}")


# Example 4: Complex multi-function query
# ========================================

print("\nExample 6: Complex query with multiple function calls")

result = llm_service.chat_with_function_calling(
    user_message="Plan a complete trip: find flights from JFK to Paris on Dec 1-15, hotels in Paris city center, and show me top attractions and activities."
)

print(f"Assistant: {result['response']}")
print(f"\nTotal function calls made: {len(result['function_calls'])}")
for i, call in enumerate(result['function_calls'], 1):
    print(f"\n{i}. Function: {call['function']}")
    print(f"   Arguments: {call['arguments']}")
    if call['result']['success']:
        data_count = len(call['result'].get('data', []))
        print(f"   Result: Success - {data_count} items returned")
    else:
        print(f"   Result: Error - {call['result'].get('error')}")


# Example 5: Location search (useful for getting IATA codes)
# ==========================================================

print("\nExample 7: Find IATA codes for a city")

result = amadeus.search_locations(
    keyword='Barcelona',
    sub_type=['CITY', 'AIRPORT']
)

if result['success']:
    print("Locations found:")
    for location in result['data'][:5]:  # Show first 5
        print(f"  - {location.get('name')} ({location.get('iataCode')}) - {location.get('subType')}")


# Example 6: Using in Django views
# =================================

"""
# In your Django view (apps/trips/views.py or similar):

from rest_framework.decorators import api_view
from rest_framework.response import Response
from services.llm_function_calling import LLMFunctionCallingService

@api_view(['POST'])
def plan_trip_with_llm(request):
    '''
    POST /api/trips/plan-with-llm/
    Body: {"message": "I want to visit Paris next month"}
    '''
    user_message = request.data.get('message')
    
    # Use LLM to process the request
    llm_service = LLMFunctionCallingService()
    result = llm_service.chat_with_function_calling(user_message=user_message)
    
    return Response({
        'response': result['response'],
        'function_calls': result['function_calls'],
        'success': result['success']
    })
"""


# Example 7: Error handling
# ==========================

print("\nExample 8: Handling API errors")

try:
    # This will fail if credentials are not set
    amadeus = AmadeusService()
    result = amadeus.search_flights(
        origin='INVALID',  # Invalid airport code
        destination='CDG',
        departure_date='2025-12-01'
    )
    
    if not result['success']:
        print(f"API Error: {result['error']}")
        # Handle error appropriately
        
except ValueError as e:
    print(f"Configuration Error: {e}")
    # Credentials not set - guide user to set them up


# Example 8: Using recommendations
# =================================

print("\nExample 9: Get travel recommendations")

result = amadeus.get_travel_recommendations(
    origin='NYC',
    max_results=5
)

if result['success']:
    print("Recommended destinations from New York:")
    for dest in result['data']:
        print(f"  - {dest.get('name')} ({dest.get('iataCode')})")


# Example 9: Points of Interest
# ==============================

print("\nExample 10: Find points of interest")

result = amadeus.search_points_of_interest(
    latitude=48.8566,  # Paris
    longitude=2.3522,
    radius=2,
    categories=['SIGHTS', 'RESTAURANT']
)

if result['success']:
    print(f"Found {len(result['data'])} points of interest:")
    for poi in result['data'][:5]:
        name = poi.get('name')
        category = poi.get('category')
        print(f"  - {name} ({category})")
