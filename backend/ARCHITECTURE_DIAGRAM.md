# Amadeus + LLM Integration Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│                    (Chat, API Clients, etc.)                    │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ Natural Language Query
                         │ "Find flights from NYC to Paris"
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DJANGO REST API                              │
│                 /api/chat/message/                              │
│              (apps/chat/views.py)                               │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ use_function_calling: true
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│             LLMFunctionCallingService                           │
│         (services/llm_function_calling.py)                      │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  1. Send message + function definitions to OpenAI GPT-4   │ │
│  │  2. GPT-4 analyzes intent and selects functions           │ │
│  │  3. Extracts parameters from natural language             │ │
│  │  4. Returns function calls to execute                     │ │
│  └───────────────────────────────────────────────────────────┘ │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ Execute function(s)
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                   AmadeusService                                │
│              (services/amadeus_service.py)                      │
│                                                                 │
│  ┌──────────────┬──────────────┬──────────────┬──────────────┐ │
│  │   Flights    │    Hotels    │  Activities  │  Locations   │ │
│  │              │              │      +       │      +       │ │
│  │ • search     │ • search_by  │     POIs     │  Transfers   │ │
│  │ • cheapest   │   _city      │              │      +       │ │
│  │ • predict    │ • search_by  │ • search     │ Recommends   │ │
│  │   delay      │   _hotels    │ • details    │              │ │
│  │              │ • ratings    │              │ • search     │ │
│  │              │ • by_name    │              │ • airports   │ │
│  └──────────────┴──────────────┴──────────────┴──────────────┘ │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ API Calls
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    AMADEUS APIS                                 │
│              (https://api.amadeus.com)                          │
│                                                                 │
│  • Flight Offers Search  • Hotel Search      • Activities      │
│  • Hotel Bookings        • POIs              • Transfers       │
│  • Travel Recommendations • Airport Info     • And more...     │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow Example

### User Query: "Find me flights and hotels for a trip to Paris next week"

```
1. USER
   ↓
   Message: "Find me flights and hotels for a trip to Paris next week"
   
2. DJANGO API (/api/chat/message/)
   ↓
   Receives message, passes to LLM service
   
3. LLM SERVICE (OpenAI GPT-4)
   ↓
   Analyzes: User wants flights AND hotels to Paris
   Determines date: ~7 days from now
   Selects functions:
   - search_locations (to get Paris code)
   - search_flights (for flight options)
   - search_hotels_by_city (for hotel options)
   
4. AMADEUS SERVICE
   ↓
   Executes 3 function calls:
   
   a) search_locations(keyword="Paris")
      → Result: PAR (city code), CDG (airport)
   
   b) search_flights(
        origin="JFK",
        destination="CDG", 
        departure_date="2025-11-29"
      )
      → Result: List of flight offers with prices
   
   c) search_hotels_by_city(
        city_code="PAR",
        check_in_date="2025-11-29",
        check_out_date="2025-12-06"
      )
      → Result: List of hotel offers
      
5. LLM SERVICE
   ↓
   Receives results, sends back to GPT-4
   GPT-4 synthesizes natural language response
   
6. USER
   ↓
   Receives formatted response:
   "I found several options for your Paris trip!
   
   Flights:
   - Air France: $650 (non-stop, 7h 30m)
   - United: $580 (1 stop, 10h 15m)
   ...
   
   Hotels:
   - Hilton Paris: $180/night (4.5★)
   - Marriott: $160/night (4.3★)
   ..."
```

## Function Categories

### 🎯 19 Functions Organized by Category

```
FLIGHTS (3)
├── search_flights           → Find flight offers
├── get_flight_cheapest_dates → Cheapest dates to fly  
└── predict_flight_delay     → Delay predictions

HOTELS (5)
├── search_hotels_by_city    → Hotels in a city
├── search_hotels_by_hotels  → Specific hotels
├── get_hotel_offer          → Offer details
├── get_hotel_ratings        → Sentiment ratings
└── search_hotel_by_name     → Name search

ACTIVITIES (2)
├── search_activities        → Tours & activities
└── get_activity_details     → Activity details

POINTS OF INTEREST (2)
├── search_points_of_interest → Landmarks, attractions
└── get_poi_details          → POI details

LOCATIONS (3)
├── search_locations         → Find airports/cities
├── get_location_details     → Location info
└── search_airports          → Nearby airports

TRANSFERS (1)
└── search_transfers         → Ground transportation

RECOMMENDATIONS (1)
└── get_travel_recommendations → Destination ideas

INFO (2)
├── lookup_airline           → Airline information
└── get_airport_routes       → Airport routes
```

## Configuration Flow

```
1. Developer Setup
   ↓
   Get API Keys:
   • Amadeus: https://developers.amadeus.com
   • OpenAI: https://platform.openai.com
   
2. Configuration File (backend/.env)
   ↓
   OPENAI_API_KEY=sk-...
   AMADEUS_CLIENT_ID=...
   AMADEUS_CLIENT_SECRET=...
   AMADEUS_HOSTNAME=test
   
3. Application Initialization
   ↓
   Services read from environment:
   • LLMFunctionCallingService → loads OpenAI key
   • AmadeusService → loads Amadeus credentials
   
4. Ready to Accept Requests
   ↓
   All 19 functions available via:
   • Direct API calls
   • LLM function calling
```

## Key Features

### ✅ Intelligent Function Selection
- LLM automatically determines which functions to call
- Can call multiple functions in sequence
- Extracts parameters from natural language

### ✅ Comprehensive Coverage
- 19 different Amadeus APIs
- Covers entire travel planning workflow
- From search to booking information

### ✅ Natural Language Interface
- Users don't need to know function names
- No need to understand parameters
- Just ask in plain English

### ✅ Error Handling
- Graceful fallbacks when APIs unavailable
- Informative error messages
- Can fallback to mock data

### ✅ Production Ready
- Environment-based configuration
- Security best practices
- Comprehensive documentation

## Technology Stack

```
Frontend Layer
└── Chat Interface / API Clients

Application Layer
├── Django 5.0.1
├── Django REST Framework 3.14.0
└── Python 3.12+

Service Layer
├── LLMFunctionCallingService
│   └── OpenAI GPT-4 Turbo
└── AmadeusService
    └── Amadeus Python SDK 8.1.0

External APIs
├── OpenAI API
│   └── Function Calling
└── Amadeus APIs
    ├── Flight Offers
    ├── Hotel Search
    ├── Activities
    └── 16 more APIs
```

## Example Interactions

### Simple Query
```
User: "Find flights to Paris"
  ↓
LLM: Calls search_locations + search_flights
  ↓
Response: List of flight options
```

### Complex Query
```
User: "Plan a complete Rome trip"
  ↓
LLM: Calls search_locations + search_flights + 
     search_hotels_by_city + search_points_of_interest
  ↓
Response: Comprehensive trip plan with flights, 
          hotels, and attractions
```

### Multi-turn Conversation
```
User: "I want to travel"
Assistant: "Where would you like to go?"

User: "Paris, next week"
Assistant: [Calls search_flights] "Here are flights..."

User: "Show me hotels too"
Assistant: [Calls search_hotels_by_city] "Here are hotels..."
```

## Benefits

### For Users
- 🗣️ Natural language queries
- 🚀 Fast, intelligent responses
- 🎯 Comprehensive travel information
- 💡 Smart recommendations

### For Developers
- 📦 Easy to use APIs
- 🔧 Well-documented functions
- 🛡️ Secure and tested
- 🔄 Easy to extend

### For Business
- 💰 Real-time pricing
- 📊 Accurate availability
- 🌍 Global coverage
- ⚡ Production ready
