# Amadeus API Integration - Function Reference

This document describes all the Amadeus API functions integrated into the application, based on the official [Amadeus Code Examples](https://github.com/amadeus4dev/amadeus-code-examples).

## Overview

The application now integrates real Amadeus Self-Service APIs through two main services:

1. **AmadeusService** (`backend/services/amadeus_service.py`) - Direct wrapper around Amadeus APIs
2. **LLMFunctionCallingService** (`backend/services/llm_function_calling.py`) - LLM-powered intelligent function calling

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `amadeus==8.1.0` - Official Amadeus Python SDK
- `openai==1.54.0` - OpenAI API for function calling

### 2. Configure API Credentials

Create a `.env` file in the `backend/` directory:

```bash
# OpenAI API (for LLM function calling)
OPENAI_API_KEY=your-openai-api-key

# Amadeus API credentials (Get from https://developers.amadeus.com)
AMADEUS_CLIENT_ID=your-amadeus-client-id
AMADEUS_CLIENT_SECRET=your-amadeus-client-secret
AMADEUS_HOSTNAME=test  # Use 'test' for testing or 'production' for production
```

To get Amadeus credentials:
1. Go to https://developers.amadeus.com
2. Sign up for a free account
3. Create a new app
4. Copy your API Key (Client ID) and API Secret (Client Secret)

## Available Functions

### Flight APIs

#### 1. `search_flights`
Search for flight offers between two locations.

**Parameters:**
- `origin` (required): IATA code of origin airport (e.g., 'JFK')
- `destination` (required): IATA code of destination airport (e.g., 'CDG')
- `departure_date` (required): Departure date in YYYY-MM-DD format
- `adults`: Number of adult travelers (default: 1)
- `return_date`: Return date for round trip
- `children`: Number of children (2-11 years)
- `infants`: Number of infants (under 2 years)
- `travel_class`: 'ECONOMY', 'PREMIUM_ECONOMY', 'BUSINESS', or 'FIRST'
- `non_stop`: Only return non-stop flights (default: False)
- `currency`: Currency code (default: 'USD')
- `max_results`: Maximum number of results (default: 250)

**Example:**
```python
from services.amadeus_service import AmadeusService

amadeus = AmadeusService()
result = amadeus.search_flights(
    origin='JFK',
    destination='CDG',
    departure_date='2025-12-01',
    adults=2,
    return_date='2025-12-15',
    travel_class='ECONOMY'
)
```

**Example user query:**
- "Find me flights from New York to Paris on December 1st"
- "I need a business class flight from LAX to London next week"

---

#### 2. `get_flight_cheapest_dates`
Find the cheapest dates to fly between two locations.

**Parameters:**
- `origin` (required): IATA code of origin airport
- `destination` (required): IATA code of destination airport
- `departure_date`: Optional departure date
- `one_way`: True for one-way, False for round-trip (default: False)

**Example user query:**
- "When is the cheapest time to fly to Paris?"
- "Find me the best flight deals to Tokyo"

---

#### 3. `predict_flight_delay`
Predict the likelihood of a flight being delayed.

**Parameters:**
- `origin`: Origin airport IATA code
- `destination`: Destination airport IATA code
- `departure_date`: Date in YYYY-MM-DD format
- `departure_time`: Time in HH:MM:SS format
- `arrival_date`: Date in YYYY-MM-DD format
- `arrival_time`: Time in HH:MM:SS format
- `airline_code`: 2-character airline IATA code
- `flight_number`: Flight number

**Example user query:**
- "Will my flight from JFK to LAX be delayed?"
- "Check delay prediction for flight AA123"

---

### Hotel APIs

#### 4. `search_hotels_by_city`
Search for hotel offers in a specific city.

**Parameters:**
- `city_code` (required): IATA city code (e.g., 'PAR' for Paris)
- `check_in_date` (required): Check-in date in YYYY-MM-DD format
- `check_out_date` (required): Check-out date in YYYY-MM-DD format
- `adults`: Number of adult guests per room (default: 1)
- `room_quantity`: Number of rooms (default: 1)
- `currency`: Currency code (default: 'USD')
- `radius`: Search radius (default: 5)
- `radius_unit`: 'KM' or 'MILE' (default: 'KM')

**Example:**
```python
result = amadeus.search_hotels_by_city(
    city_code='PAR',
    check_in_date='2025-12-01',
    check_out_date='2025-12-05',
    adults=2,
    room_quantity=1
)
```

**Example user query:**
- "Find hotels in Paris for December 1-5"
- "I need a hotel room in London for 3 nights"

---

#### 5. `search_hotels_by_hotels`
Search for specific hotels by their IDs.

**Parameters:**
- `hotel_ids` (required): List of Amadeus hotel IDs
- `check_in_date` (required): Check-in date
- `check_out_date` (required): Check-out date
- `adults`: Number of guests (default: 1)
- `room_quantity`: Number of rooms (default: 1)

---

#### 6. `get_hotel_offer`
Get details of a specific hotel offer.

**Parameters:**
- `offer_id` (required): Amadeus hotel offer ID

---

#### 7. `get_hotel_ratings`
Get sentiment analysis ratings for hotels.

**Parameters:**
- `hotel_ids` (required): List of Amadeus hotel IDs (max 3)

**Example user query:**
- "What are the ratings for the Hilton Paris?"
- "Show me reviews for hotels in Rome"

---

#### 8. `search_hotel_by_name`
Search hotels by name (autocomplete).

**Parameters:**
- `keyword` (required): Search keyword (hotel name)
- `sub_type`: List of location subtypes

**Example user query:**
- "Find Marriott hotels"
- "Search for Ritz-Carlton"

---

### Activities & Points of Interest APIs

#### 9. `search_activities`
Search for tours and activities at a specific location.

**Parameters:**
- `latitude` (required): Latitude coordinate
- `longitude` (required): Longitude coordinate
- `radius`: Search radius in km (1-20, default: 1)

**Example:**
```python
result = amadeus.search_activities(
    latitude=48.8566,
    longitude=2.3522,
    radius=5
)
```

**Example user query:**
- "What activities are available in Paris?"
- "Show me tours near the Eiffel Tower"
- "Find things to do in Barcelona"

---

#### 10. `search_points_of_interest`
Search for points of interest (landmarks, attractions, restaurants).

**Parameters:**
- `latitude` (required): Latitude coordinate
- `longitude` (required): Longitude coordinate
- `radius`: Search radius in km (default: 1)
- `categories`: List of POI categories (e.g., ['SIGHTS', 'NIGHTLIFE', 'RESTAURANT'])

**Example user query:**
- "What are the top attractions in Paris?"
- "Show me restaurants near Times Square"
- "Find nightlife in Barcelona"

---

#### 11. `get_activity_details`
Get details of a specific activity.

**Parameters:**
- `activity_id` (required): Amadeus activity ID

---

#### 12. `get_poi_details`
Get details of a specific point of interest.

**Parameters:**
- `poi_id` (required): POI ID

---

### Location APIs

#### 13. `search_locations`
Search for airports, cities, and locations by keyword.

**Parameters:**
- `keyword` (required): Search keyword
- `sub_type`: List of location types (e.g., ['AIRPORT', 'CITY'])
- `view`: 'LIGHT' or 'FULL' (default: 'FULL')

**Example:**
```python
result = amadeus.search_locations(
    keyword='Paris',
    sub_type=['CITY', 'AIRPORT']
)
```

**Example user query:**
- "What's the airport code for Paris?"
- "Find airports near New York"
- "Search for cities starting with 'Rome'"

---

#### 14. `get_location_details`
Get details of a specific location.

**Parameters:**
- `location_id` (required): Location ID

---

#### 15. `search_airports`
Search for nearest airports by coordinates.

**Parameters:**
- `latitude` (required): Latitude coordinate
- `longitude` (required): Longitude coordinate
- `radius`: Search radius in km (default: 500)

**Example user query:**
- "What airports are near me?"
- "Find airports within 100km of London"

---

### Transfer APIs

#### 16. `search_transfers`
Search for ground transfers (taxis, shuttles, private cars).

**Parameters:**
- `start_latitude` (required): Starting point latitude
- `start_longitude` (required): Starting point longitude
- `end_latitude` (required): Destination latitude
- `end_longitude` (required): Destination longitude
- `start_date_time` (required): Pickup date/time in ISO format
- `passengers`: Number of passengers (default: 1)
- `start_address_line`: Starting address (optional)
- `end_address_line`: Destination address (optional)

**Example user query:**
- "Book a transfer from the airport to my hotel"
- "I need a car from JFK to Manhattan"

---

### Recommendations APIs

#### 17. `get_travel_recommendations`
Get AI-powered travel destination recommendations.

**Parameters:**
- `origin` (required): Origin city IATA code
- `destination_country`: Optional destination country code
- `max_results`: Maximum number of recommendations (default: 10)

**Example user query:**
- "Where should I travel from New York?"
- "Recommend destinations from London"
- "Suggest places to visit from Tokyo"

---

### Airline & Airport Info APIs

#### 18. `lookup_airline`
Look up airline information by code.

**Parameters:**
- `airline_code` (required): 2-letter IATA airline code

**Example user query:**
- "What airline is AA?"
- "Tell me about Delta Airlines"

---

#### 19. `get_airport_routes`
Get all routes departing from an airport.

**Parameters:**
- `airport_code` (required): 3-letter IATA airport code
- `max_results`: Maximum number of routes (default: 50)

**Example user query:**
- "Where can I fly from JFK?"
- "Show me all routes from London Heathrow"

---

## Using LLM Function Calling

The LLM Function Calling service automatically:
1. Understands user intent
2. Determines which Amadeus function(s) to call
3. Extracts parameters from natural language
4. Calls the appropriate functions
5. Synthesizes the results into a natural response

### Example via Chat API

```bash
curl -X POST http://localhost:8000/api/chat/message/ \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I want to fly from New York to Paris on December 1st, coming back on December 15th. Show me business class options.",
    "use_function_calling": true
  }'
```

The LLM will:
1. Understand the request
2. Call `search_locations` to get IATA codes (if needed)
3. Call `search_flights` with the appropriate parameters
4. Return a formatted response with flight options

### Direct Service Usage

```python
from services.llm_function_calling import LLMFunctionCallingService

# Initialize service
llm_service = LLMFunctionCallingService()

# Process a user query
result = llm_service.chat_with_function_calling(
    user_message="Find me hotels in Paris for next week"
)

print(result['response'])  # Natural language response
print(result['function_calls'])  # Functions that were called
```

## Common IATA Codes

### Cities
- **PAR** - Paris
- **LON** - London
- **NYC** - New York City
- **LAX** - Los Angeles
- **ROM** - Rome
- **BCN** - Barcelona
- **TYO** - Tokyo
- **DXB** - Dubai
- **SIN** - Singapore

### Airports
- **JFK** - New York JFK
- **LAX** - Los Angeles
- **CDG** - Paris Charles de Gaulle
- **LHR** - London Heathrow
- **FCO** - Rome Fiumicino
- **NRT** - Tokyo Narita
- **DXB** - Dubai International

## Error Handling

All functions return a dictionary with:
```python
{
    'success': True/False,
    'data': {...},  # If success=True
    'error': '...'  # If success=False
}
```

## Testing

To test the integration:

1. **Set up credentials** in `.env` file
2. **Run the Django server:**
   ```bash
   cd backend
   python manage.py runserver
   ```
3. **Test via chat endpoint:**
   ```bash
   curl -X POST http://localhost:8000/api/chat/message/ \
     -H "Content-Type: application/json" \
     -d '{"message": "Find flights from JFK to CDG on 2025-12-01"}'
   ```

## Migration from Mock Data

The application previously used mock data in:
- `flight_provider.py` - Now can use `AmadeusService.search_flights()`
- `hotel_provider.py` - Now can use `AmadeusService.search_hotels_by_city()`
- `itinerary_generator.py` - Can use `AmadeusService.search_activities()` and `search_points_of_interest()`

You can gradually migrate from mock to real data, or use real data when API credentials are available and fallback to mocks otherwise.

## Resources

- **Amadeus for Developers**: https://developers.amadeus.com
- **Amadeus Code Examples**: https://github.com/amadeus4dev/amadeus-code-examples
- **Amadeus Python SDK**: https://github.com/amadeus4dev/amadeus-python
- **OpenAI Function Calling**: https://platform.openai.com/docs/guides/function-calling

## Support

For issues with:
- **Amadeus APIs**: Check https://developers.amadeus.com or their Discord
- **OpenAI APIs**: Check https://platform.openai.com/docs
- **This Integration**: Open an issue in the repository
