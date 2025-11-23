# OpenRouter Function Calling - Test Examples

## Quick Test Commands

### 1. Basic Flight Search
```bash
curl -X POST http://localhost:8000/api/chat/functions/ \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I want to fly from Bucharest to Paris on December 1st"
  }'
```

**Expected Functions Called:**
- `search_locations` (for Bucharest and Paris)
- `search_flights` (with OTP → CDG)

---

### 2. Cheapest Flights Query (Romanian)
```bash
curl -X POST http://localhost:8000/api/chat/functions/ \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Vreau să merg în noiembrie și să văd cele mai ieftine zboruri la Paris"
  }'
```

**Expected Functions Called:**
- `search_locations` (for Paris)
- `get_flight_cheapest_dates` (for November dates)

---

### 3. Hotel Search
```bash
curl -X POST http://localhost:8000/api/chat/functions/ \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Find hotels in Barcelona for 3 nights starting December 10th"
  }'
```

**Expected Functions Called:**
- `search_locations` (for Barcelona)
- `search_hotels_by_city` (BCN, check-in: 2025-12-10, check-out: 2025-12-13)

---

### 4. Activities Search
```bash
curl -X POST http://localhost:8000/api/chat/functions/ \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What can I do in Paris?"
  }'
```

**Expected Functions Called:**
- `search_locations` (for Paris coordinates)
- `search_activities` (lat/lon of Paris)
- `search_points_of_interest` (lat/lon of Paris)

---

### 5. Airline Lookup (Romanian)
```bash
curl -X POST http://localhost:8000/api/chat/functions/ \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Ce companie aeriană este RO?"
  }'
```

**Expected Functions Called:**
- `lookup_airline` (airline_code: "RO")

---

### 6. Airport Routes
```bash
curl -X POST http://localhost:8000/api/chat/functions/ \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Where can I fly from Bucharest airport?"
  }'
```

**Expected Functions Called:**
- `search_locations` (for Bucharest to get OTP)
- `get_airport_routes` (airport_code: "OTP")

---

### 7. Travel Recommendations
```bash
curl -X POST http://localhost:8000/api/chat/functions/ \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Recommend me some destinations from Bucharest"
  }'
```

**Expected Functions Called:**
- `search_locations` (for Bucharest to get OTP)
- `get_travel_recommendations` (origin: "OTP")

---

### 8. Multi-turn Conversation (Context Test)
```bash
# First message
curl -X POST http://localhost:8000/api/chat/functions/ \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I want to go to Paris"
  }'

# Save the session_id from response, then:

# Second message (references previous context)
curl -X POST http://localhost:8000/api/chat/functions/ \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "SESSION_ID_FROM_FIRST_RESPONSE",
    "message": "Show me the cheapest flights in November"
  }'
```

**Expected Behavior:**
- First message: LLM asks for more details (dates, etc.)
- Second message: LLM remembers Paris, searches flights for November

---

### 9. Complex Query (Multiple Functions)
```bash
curl -X POST http://localhost:8000/api/chat/functions/ \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I want to go to Rome, find me the cheapest flights and hotels for 5 nights"
  }'
```

**Expected Functions Called:**
- `search_locations` (for Rome)
- `get_flight_cheapest_dates` (to Rome)
- `search_hotels_by_city` (ROM, 5 nights)

---

### 10. Romanian Complex Query
```bash
curl -X POST http://localhost:8000/api/chat/functions/ \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Vreau să merg undeva în weekend, sugerează-mi destinații și arată-mi cele mai ieftine zboruri"
  }'
```

**Expected Functions Called:**
- Needs origin (LLM will ask or assume)
- `get_travel_recommendations` (for destination suggestions)
- `get_flight_cheapest_dates` (for cheap flights)

---

## Expected Response Format

```json
{
  "session_id": "uuid-string",
  "message": "Natural language response from LLM with travel information",
  "function_calls": [
    {
      "function": "search_locations",
      "arguments": {
        "keyword": "Paris",
        "sub_type": ["CITY", "AIRPORT"]
      },
      "result": {
        "success": true,
        "data": [
          {
            "type": "location",
            "subType": "CITY",
            "name": "PARIS",
            "iataCode": "PAR",
            ...
          }
        ]
      }
    },
    {
      "function": "get_flight_cheapest_dates",
      "arguments": {
        "origin": "OTP",
        "destination": "CDG"
      },
      "result": {
        "success": true,
        "data": [...]
      }
    }
  ],
  "success": true,
  "messages": [
    {
      "role": "user",
      "content": "Original user message",
      "created_at": "2025-11-22T..."
    },
    {
      "role": "assistant",
      "content": "LLM response",
      "created_at": "2025-11-22T..."
    }
  ]
}
```

---

## Testing Checklist

### Basic Functionality
- [ ] Flight search works with city names (not just IATA codes)
- [ ] Cheapest dates query returns data
- [ ] Hotel search works
- [ ] Activity search works
- [ ] Airline lookup works
- [ ] Airport routes works

### Natural Language Understanding
- [ ] Understands Romanian queries
- [ ] Understands English queries
- [ ] Handles vague requests (e.g., "I want to travel somewhere")
- [ ] Interprets relative dates (e.g., "next month", "in November")
- [ ] Understands multiple requests in one message

### Context & Sessions
- [ ] Creates new session on first message
- [ ] Reuses session on subsequent messages
- [ ] Maintains conversation history
- [ ] References previous context correctly
- [ ] Can handle multi-turn conversations

### Error Handling
- [ ] Handles missing API keys gracefully
- [ ] Returns friendly errors for invalid cities
- [ ] Handles Amadeus API errors
- [ ] Provides helpful suggestions when request is unclear

### Function Calling
- [ ] Calls correct function for each query type
- [ ] Calls multiple functions when needed
- [ ] Passes correct arguments to functions
- [ ] Chains functions appropriately (e.g., location lookup → flight search)
- [ ] Handles function execution failures

---

## Common Issues & Solutions

### Issue: "OpenRouter API key not provided"
**Solution:** Set `OPENROUTER_API_KEY` in `.env` file

### Issue: "Amadeus API credentials not provided"
**Solution:** Set `AMADEUS_CLIENT_ID` and `AMADEUS_CLIENT_SECRET` in `.env`

### Issue: No response or timeout
**Solution:** 
- Check OpenRouter account has credits
- Verify network connectivity
- Increase timeout if needed

### Issue: Wrong IATA codes returned
**Solution:** LLM should call `search_locations` first; if not, check function descriptions

### Issue: Context not maintained
**Solution:** Ensure using same `session_id` in subsequent requests

---

## Performance Benchmarks

Expected response times:
- Simple query (1 function): 2-4 seconds
- Complex query (2-3 functions): 4-8 seconds
- Very complex query (4+ functions): 8-15 seconds

Cost estimates (OpenRouter):
- Simple query: ~$0.01
- Complex query: ~$0.02-0.05
- Very complex query: ~$0.05-0.10

---

## Python Test Script

```python
import requests
import json

BASE_URL = "http://localhost:8000/api/chat/functions/"

def test_flight_search():
    """Test basic flight search"""
    response = requests.post(BASE_URL, json={
        "message": "I want to fly from Bucharest to Paris on December 1st"
    })
    
    data = response.json()
    print("Response:", json.dumps(data, indent=2))
    
    # Verify function calls
    assert data['success'] == True
    assert len(data['function_calls']) > 0
    assert any(fc['function'] == 'search_flights' for fc in data['function_calls'])

def test_cheapest_dates():
    """Test cheapest dates query"""
    response = requests.post(BASE_URL, json={
        "message": "When is the cheapest time to fly to Barcelona?"
    })
    
    data = response.json()
    print("Response:", json.dumps(data, indent=2))
    
    assert data['success'] == True
    assert any(fc['function'] == 'get_flight_cheapest_dates' for fc in data['function_calls'])

def test_hotel_search():
    """Test hotel search"""
    response = requests.post(BASE_URL, json={
        "message": "Find hotels in Rome for 3 nights starting December 10th"
    })
    
    data = response.json()
    print("Response:", json.dumps(data, indent=2))
    
    assert data['success'] == True
    assert any(fc['function'] == 'search_hotels_by_city' for fc in data['function_calls'])

def test_conversation_context():
    """Test multi-turn conversation"""
    # First message
    response1 = requests.post(BASE_URL, json={
        "message": "I want to go to Paris"
    })
    data1 = response1.json()
    session_id = data1['session_id']
    
    # Second message with context
    response2 = requests.post(BASE_URL, json={
        "session_id": session_id,
        "message": "Show me hotels for 3 nights"
    })
    data2 = response2.json()
    
    print("First response:", data1['message'])
    print("Second response:", data2['message'])
    
    # LLM should remember Paris from first message
    assert session_id == data2['session_id']

if __name__ == "__main__":
    print("Testing OpenRouter Function Calling...")
    print("\n1. Testing flight search...")
    test_flight_search()
    
    print("\n2. Testing cheapest dates...")
    test_cheapest_dates()
    
    print("\n3. Testing hotel search...")
    test_hotel_search()
    
    print("\n4. Testing conversation context...")
    test_conversation_context()
    
    print("\n✅ All tests passed!")
```

Save as `test_function_calling.py` and run:
```bash
cd backend
python ../test_function_calling.py
```

---

## Monitoring & Debugging

### Enable Debug Logging
In `backend/config/settings.py`, add:
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
```

### View Function Calls
Check the `function_calls` array in the response to see exactly what functions were called and with what arguments.

### Check Session State
```bash
# Get session details
curl http://localhost:8000/api/chat/session/SESSION_ID/
```

---

## Advanced Usage

### Custom System Message
Modify `openrouter_function_calling.py` line 370 to customize the LLM's behavior.

### Add More Functions
1. Add function to `amadeus_service.py`
2. Add function definition to `get_function_definitions()` in `openrouter_function_calling.py`
3. Map function in `execute_function()` method

### Change LLM Model
Modify `self.model` in `openrouter_function_calling.py` to use different models:
- `anthropic/claude-3.5-sonnet` (current)
- `anthropic/claude-3-opus`
- `openai/gpt-4-turbo`

---

## Production Checklist

Before deploying to production:
- [ ] Use production Amadeus credentials (`AMADEUS_HOSTNAME=production`)
- [ ] Set up rate limiting
- [ ] Implement caching for repeated queries
- [ ] Add monitoring and alerting
- [ ] Set up error tracking (e.g., Sentry)
- [ ] Optimize timeout settings
- [ ] Add authentication/authorization
- [ ] Review and optimize token usage
- [ ] Set up backup for session data
- [ ] Test under load
