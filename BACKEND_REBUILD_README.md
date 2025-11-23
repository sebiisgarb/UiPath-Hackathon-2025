# Travel Chatbot Backend - Rebuilt Architecture

## Overview

This is a complete rebuild of the travel chatbot backend using Django with OpenRouter (Claude Sonnet 4) and Amadeus APIs. The backend implements a tool-based execution flow where the LLM uses function calling to interact with real Amadeus travel APIs.

## Architecture

```
backend/
├── apps/
│   └── chat/               # Main chat application
│       ├── views.py        # Chat and reset endpoints
│       └── urls.py         # URL routing
├── services/
│   ├── chatbot_service.py        # Conversation orchestration with tool-calling
│   ├── openrouter_service.py     # OpenRouter/Claude API client
│   ├── amadeus_tool_service.py   # Amadeus API wrappers
│   └── amadeus_service.py        # Base Amadeus service
└── config/
    ├── settings.py         # Django settings
    └── urls.py             # Main URL configuration
```

## Key Features

### 1. Tool-Based Execution Flow
- LLM sends tool_call requests
- Backend executes corresponding Amadeus API calls
- Results returned to LLM for processing
- LLM continues until producing final answer

### 2. Conversation Management
- In-memory session storage
- Maintains conversation history
- Tracks state: origin_airport, destination_airport, departure_date, return_date, adults, children

### 3. 15+ Amadeus API Tools
All tools are exposed to the LLM via OpenAI function-calling format:

**Location/Airport:**
- `airport_city_search` - Search airports and cities
- `airport_direct_destinations` - Get direct destinations from airport
- `airline_destinations` - Get airline destination network

**Flights:**
- `flight_offers_search` - Search flight offers
- `flight_inspiration_search` - Get destination inspiration
- `flight_cheapest_date_search` - Find cheapest travel dates
- `flight_offers_price` - Get confirmed pricing
- `trip_purpose_prediction` - Predict trip purpose (business/leisure)

**Hotels:**
- `hotel_list` - List hotels in a city
- `hotel_search` - Search hotel offers
- `hotel_offers_by_hotel` - Get specific hotel offers
- `hotel_ratings` - Get hotel ratings/sentiment

**Activities:**
- `tours_and_activities` - Search activities by coordinates
- `tours_and_activities_by_square` - Search activities by bounding box
- `get_activity_details` - Get activity details

## API Endpoints

### POST /chat
Main chat endpoint with tool-calling orchestration.

**Request:**
```json
{
  "message": "I want to fly from New York to Paris next month",
  "sessionId": "optional-session-id"
}
```

**Response:**
```json
{
  "reply": "I'll help you find flights from New York to Paris...",
  "state": {
    "origin_airport": "JFK",
    "destination_airport": "CDG",
    "departure_date": "2025-12-15",
    "return_date": null,
    "adults": 1,
    "children": 0
  },
  "history": [...],
  "session_id": "uuid-session-id"
}
```

### POST /chat/reset
Reset a chat session.

**Request:**
```json
{
  "sessionId": "session-id-to-reset"
}
```

**Response:**
```json
{
  "message": "Session reset successful"
}
```

## Environment Variables

Required environment variables (set in `.env` file):

```bash
# OpenRouter API (Required)
OPENROUTER_API_KEY=your-openrouter-api-key

# Amadeus API (Required)
AMADEUS_CLIENT_ID=your-amadeus-client-id
AMADEUS_CLIENT_SECRET=your-amadeus-client-secret
AMADEUS_HOSTNAME=test  # 'test' or 'production'

# Django
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

## Installation & Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set up environment variables:**
```bash
cp backend/.env.example backend/.env
# Edit .env with your API keys
```

3. **Run migrations:**
```bash
cd backend
python manage.py migrate
```

4. **Start the server:**
```bash
python manage.py runserver
```

The server will start on `http://localhost:8000`

## Usage Example

### Using curl:

```bash
# Start a conversation
curl -X POST http://localhost:8000/chat/ \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I want to travel from San Francisco to Tokyo in January"
  }'

# Continue conversation with session ID
curl -X POST http://localhost:8000/chat/ \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Show me flights for 2 adults",
    "sessionId": "session-id-from-previous-response"
  }'

# Reset session
curl -X POST http://localhost:8000/chat/reset/ \
  -H "Content-Type: application/json" \
  -d '{
    "sessionId": "session-id-to-reset"
  }'
```

### Using Python:

```python
import requests

# Chat endpoint
response = requests.post('http://localhost:8000/chat/', json={
    'message': 'Find me hotels in Paris for next week'
})

print(response.json())
# {
#   "reply": "I'll help you find hotels in Paris...",
#   "state": {...},
#   "history": [...],
#   "session_id": "..."
# }
```

## How It Works

1. **User sends a message** to `/chat/`
2. **ChatbotService** prepares messages with system prompt and conversation history
3. **OpenRouterService** sends request to Claude Sonnet 4 with tool definitions
4. **If Claude requests tools:**
   - Extract tool calls from response
   - Execute each tool via **AmadeusToolService**
   - Add tool results to conversation
   - Send updated conversation back to Claude
   - Repeat until Claude provides final answer
5. **Return final answer** with updated state to user

## Changes from Original Backend

### Removed:
- `apps/trips/` - Trip planning app (replaced by chatbot)
- `apps/integrations/` - External integrations app (not needed)
- `services/travel_planning_service.py` - Old workflow service
- `services/llm_parser.py` - Old LLM parser
- `services/flight_provider.py` - Mock flight provider
- `services/hotel_provider.py` - Mock hotel provider
- `services/itinerary_generator.py` - Itinerary generator
- Old chat models and database logic

### Added:
- `services/chatbot_service.py` - New conversation orchestration
- `services/openrouter_service.py` - OpenRouter API client
- `services/amadeus_tool_service.py` - Enhanced Amadeus wrappers
- Tool-calling loop implementation
- In-memory session management
- Simplified endpoint structure

### Kept:
- `services/amadeus_service.py` - Base Amadeus API integration
- `apps/chat/` - Chat app structure (views updated)
- Django configuration
- Database models (for potential future persistence)

## Testing

The backend can be tested with API keys from:
- **OpenRouter**: https://openrouter.ai/ (requires credits)
- **Amadeus**: https://developers.amadeus.com/ (free test environment)

## Notes

- Sessions are stored in-memory and will be lost on server restart
- For production, implement persistent session storage (Redis, database)
- The current implementation uses Claude Sonnet 4 via OpenRouter
- All Amadeus API calls are real and use the official SDK
- Maximum 10 tool-calling iterations per conversation turn to prevent loops

## Support

For issues or questions about the Amadeus APIs, refer to:
- Amadeus documentation: https://developers.amadeus.com/
- OpenRouter documentation: https://openrouter.ai/docs
