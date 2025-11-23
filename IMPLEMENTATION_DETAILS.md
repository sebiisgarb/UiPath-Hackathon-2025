# Summary: OpenRouter Function Calling Implementation

## What We Built

A comprehensive LLM-powered travel assistant that uses OpenRouter (Claude Sonnet 4.5) to understand natural language queries and automatically call the appropriate Amadeus API functions.

## Key Components

### 1. New Service: `openrouter_function_calling.py`
- Replaces OpenAI dependency with OpenRouter
- Supports 14 Amadeus API functions
- Maintains conversation context across sessions
- Intelligent function chaining (can call multiple functions in sequence)

### 2. New Endpoint: `POST /api/chat/functions/`
- Natural language interface to all Amadeus APIs
- Session-based conversation with context memory
- Returns both AI response and function call details

### 3. Updated Files
- **requirements.txt**: Removed `openai==1.54.0`
- **apps/chat/views.py**: Added `chat_with_functions` view
- **apps/chat/urls.py**: Added `/functions/` endpoint

## What We Removed

- ❌ OpenAI dependency (`openai==1.54.0`)
- ❌ Need for separate function calling service using OpenAI

## What We Kept

- ✅ `llm_function_calling.py` - Still available for OpenAI users
- ✅ `travel_planning_service.py` - Original workflow-based planning
- ✅ All Amadeus SDK integration
- ✅ Existing endpoints (backward compatible)

## Supported Functions (14 total)

### Flights (3)
1. `search_flights` - Find flight offers
2. `get_flight_cheapest_dates` - Find cheapest travel dates
3. `predict_flight_delay` - Predict flight delays

### Hotels (3)
4. `search_hotels_by_city` - Find hotels by city
5. `get_hotel_ratings` - Get hotel ratings/reviews
6. `search_hotel_by_name` - Search hotels by name

### Activities & POI (2)
7. `search_activities` - Find tours and activities
8. `search_points_of_interest` - Find landmarks, restaurants

### Locations (2)
9. `search_locations` - Find airports/cities by keyword
10. `search_airports` - Find nearest airports by coordinates

### Transfers (1)
11. `search_transfers` - Find ground transportation

### Recommendations (1)
12. `get_travel_recommendations` - Get AI destination suggestions

### Info (2)
13. `lookup_airline` - Look up airline by code
14. `get_airport_routes` - Get routes from airport

## Natural Language Examples

The LLM understands various phrasings:

### Romanian (Native)
- "Vreau să merg în noiembrie la Paris și să văd cele mai ieftine zboruri"
- "Găsește-mi hoteluri în București pentru 3 nopți"
- "Ce pot să fac în Paris?"

### English
- "I want to go in November and show me the cheapest flights"
- "Find flights from Bucharest to Paris on December 1st"
- "What can I do in Barcelona?"
- "When is the cheapest time to fly to Rome?"

## API Usage

### Basic Request
```bash
curl -X POST http://localhost:8000/api/chat/functions/ \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I want to go to Paris in November, show me the cheapest flights"
  }'
```

### With Session (Maintains Context)
```bash
# First message
curl -X POST http://localhost:8000/api/chat/functions/ \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I want to go to Paris"
  }'

# Response includes session_id
# Second message uses session_id to maintain context
curl -X POST http://localhost:8000/api/chat/functions/ \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "uuid-from-previous-response",
    "message": "When are the cheapest dates in November?"
  }'
```

### Response Format
```json
{
  "session_id": "abc-123-def",
  "message": "Based on my search, the cheapest dates to fly to Paris in November are...",
  "function_calls": [
    {
      "function": "search_locations",
      "arguments": {"keyword": "Paris", "sub_type": ["CITY", "AIRPORT"]},
      "result": {"success": true, "data": [...]}
    },
    {
      "function": "get_flight_cheapest_dates",
      "arguments": {"origin": "OTP", "destination": "CDG"},
      "result": {"success": true, "data": [...]}
    }
  ],
  "success": true,
  "messages": [...]
}
```

## Configuration Required

### Environment Variables (.env file)
```bash
# OpenRouter (Required)
OPENROUTER_API_KEY=sk-or-v1-...

# Amadeus (Required)
AMADEUS_CLIENT_ID=your-client-id
AMADEUS_CLIENT_SECRET=your-client-secret
AMADEUS_HOSTNAME=test
```

### Where to Get Keys
- **OpenRouter**: https://openrouter.ai/ (requires funding)
- **Amadeus**: https://developers.amadeus.com/ (free test account)

## How It Works

1. **User sends natural language query** (in any language)
2. **LLM analyzes intent** and determines needed functions
3. **Automatic IATA code lookup** if user provides city names
4. **Function execution** calls Amadeus APIs
5. **LLM synthesizes results** into natural language response
6. **Context saved** in chat session for follow-up queries

## Intelligent Features

### 1. Code Resolution
```
User: "I want to fly to Paris"
LLM: Calls search_locations("Paris") → Gets CDG, ORY codes
```

### 2. Date Interpretation
```
User: "in November"
LLM: Interprets as November 2025, handles flexible dates
```

### 3. Function Chaining
```
User: "Find hotels in Paris for 3 nights"
LLM: 
  1. search_locations("Paris") → Get PAR code
  2. search_hotels_by_city(PAR, check_in, check_out)
```

### 4. Context Awareness
```
User: "I want to go to Paris"
LLM: "When would you like to travel?"
User: "In November"
LLM: Remembers Paris, searches November dates
```

## Benefits

✅ **No More Rigid Commands** - Natural conversation
✅ **Multi-language Support** - Works in Romanian, English, etc.
✅ **Context Memory** - Remembers previous messages
✅ **Intelligent Routing** - Picks right function automatically
✅ **Complete Coverage** - All 14 Amadeus functions available
✅ **Single Provider** - OpenRouter only (no OpenAI needed)

## Testing Checklist

- [ ] Test flight search with city names
- [ ] Test cheapest dates query
- [ ] Test hotel search
- [ ] Test activity search
- [ ] Test airline lookup
- [ ] Test airport routes
- [ ] Test conversation context (multi-turn)
- [ ] Test error handling (invalid cities, dates)
- [ ] Test in Romanian language
- [ ] Test complex multi-function queries

## Architecture Diagram

```
┌─────────────┐
│    User     │
└──────┬──────┘
       │ Natural Language Query
       ↓
┌─────────────────────────────────┐
│  POST /api/chat/functions/      │
│  (Django View)                  │
└──────┬──────────────────────────┘
       │
       ↓
┌──────────────────────────────────────┐
│  OpenRouterFunctionCallingService   │
│  - Parse intent                     │
│  - Get function definitions         │
│  - Manage conversation context      │
└──────┬───────────────────────────────┘
       │
       ↓
┌──────────────────────────┐
│   OpenRouter API         │
│   (Claude Sonnet 4.5)    │
│   - Function calling     │
│   - Tool selection       │
└──────┬───────────────────┘
       │
       ↓
┌──────────────────────────┐
│   Amadeus Service        │
│   - 14 API functions     │
│   - Real travel data     │
└──────┬───────────────────┘
       │
       ↓
┌──────────────────────────┐
│   Response Synthesis     │
│   - Natural language     │
│   - Context update       │
│   - Session save         │
└──────────────────────────┘
```

## Documentation

- **Main Guide**: `backend/OPENROUTER_FUNCTION_CALLING.md`
- **Amadeus Functions**: `backend/AMADEUS_FUNCTIONS.md`
- **API Examples**: `backend/API_EXAMPLES.md`

## Next Steps

To use this system:

1. Set environment variables in `.env`
2. Run Django server: `python manage.py runserver`
3. Send POST requests to `/api/chat/functions/`
4. Test with various natural language queries
5. Verify function calls in response
6. Check conversation context persistence

## Cost Estimate

- **OpenRouter (Claude Sonnet 4.5)**: ~$0.01-0.05 per request
- **Amadeus Test API**: Free
- **Amadeus Production API**: Varies by usage

## Support

For issues:
- Check `.env` configuration
- Verify API keys are valid
- Check logs for detailed errors
- Review `OPENROUTER_FUNCTION_CALLING.md`
