# Amadeus Integration - Quick Reference Card

## 🎯 Quick Commands

### Install & Setup
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Get credentials (both free!)
# Amadeus: https://developers.amadeus.com
# OpenAI: https://platform.openai.com

# 3. Configure .env (in backend/ folder)
cat > backend/.env << EOF
OPENAI_API_KEY=your-openai-key-here
AMADEUS_CLIENT_ID=your-amadeus-id
AMADEUS_CLIENT_SECRET=your-amadeus-secret
AMADEUS_HOSTNAME=test
EOF

# 4. Run server
cd backend && python manage.py runserver
```

### Test Commands
```bash
# Simple flight search
curl -X POST http://localhost:8000/api/chat/message/ \
  -H "Content-Type: application/json" \
  -d '{"message": "Find flights from NYC to Paris", "use_function_calling": true}'

# Hotel search
curl -X POST http://localhost:8000/api/chat/message/ \
  -H "Content-Type: application/json" \
  -d '{"message": "Find hotels in Paris for Dec 1-5", "use_function_calling": true}'

# Complex query
curl -X POST http://localhost:8000/api/chat/message/ \
  -H "Content-Type: application/json" \
  -d '{"message": "Plan a trip to Rome: flights, hotels, and attractions", "use_function_calling": true}'
```

## 📚 19 Available Functions

### Flights ✈️
1. `search_flights` - Find flight offers
2. `get_flight_cheapest_dates` - Cheapest dates to fly
3. `predict_flight_delay` - Delay predictions

### Hotels 🏨
4. `search_hotels_by_city` - Hotels in a city
5. `search_hotels_by_hotels` - Specific hotels
6. `get_hotel_offer` - Hotel offer details
7. `get_hotel_ratings` - Hotel ratings
8. `search_hotel_by_name` - Search by name

### Activities 🎭
9. `search_activities` - Tours & activities
10. `get_activity_details` - Activity details

### Points of Interest 📍
11. `search_points_of_interest` - Landmarks, attractions
12. `get_poi_details` - POI details

### Locations 🌍
13. `search_locations` - Find airports/cities
14. `get_location_details` - Location info
15. `search_airports` - Nearby airports

### Other 🚗
16. `search_transfers` - Ground transportation
17. `get_travel_recommendations` - Destination ideas
18. `lookup_airline` - Airline info
19. `get_airport_routes` - Airport routes

## 💻 Code Examples

### Direct API Call
```python
from services.amadeus_service import AmadeusService

amadeus = AmadeusService()
result = amadeus.search_flights(
    origin='JFK',
    destination='CDG',
    departure_date='2025-12-01',
    adults=2
)
```

### LLM Function Calling
```python
from services.llm_function_calling import LLMFunctionCallingService

llm = LLMFunctionCallingService()
result = llm.chat_with_function_calling(
    user_message="Find me hotels in Paris for next week"
)
print(result['response'])
```

## 🔑 Common IATA Codes

### Cities
- NYC (New York), LAX (Los Angeles), CHI (Chicago)
- PAR (Paris), LON (London), ROM (Rome), BCN (Barcelona)
- TYO (Tokyo), SIN (Singapore), DXB (Dubai)

### Airports
- JFK (New York JFK), LAX (Los Angeles)
- CDG (Paris Charles de Gaulle), LHR (London Heathrow)
- FCO (Rome Fiumicino), NRT (Tokyo Narita)

**Find codes:** Use `search_locations(keyword='Paris')` function

## 🐛 Troubleshooting

| Error | Solution |
|-------|----------|
| "Amadeus API credentials not provided" | Set credentials in backend/.env |
| "OpenAI API key not provided" | Add OPENAI_API_KEY to .env |
| ResponseError from Amadeus | Check credentials, verify IATA codes |
| Mock data still showing | Set use_function_calling: true |

## 📊 API Limits

**Amadeus Test (Free):**
- 2,000 calls/month for flights
- 2,000 calls/month for hotels
- 10 calls/second rate limit

**OpenAI:**
- Pay-per-use (GPT-4 Turbo)
- ~$0.01-0.03 per 1K tokens

## 📖 Documentation Files

- `AMADEUS_INTEGRATION_README.md` - Complete setup guide
- `AMADEUS_FUNCTIONS.md` - Full function reference
- `USAGE_EXAMPLES.py` - Code examples
- This file - Quick reference

## 💡 Example Queries

The LLM understands natural language:

✅ "Find me flights from New York to Paris"
✅ "Show hotels in Barcelona for next weekend"
✅ "What attractions are in Rome?"
✅ "I need a complete trip: flights, hotel, activities"
✅ "When is the cheapest time to fly to Tokyo?"
✅ "Find transfers from airport to downtown"
✅ "Recommend destinations from London"

## 🎯 Architecture Flow

```
User Query
    ↓
POST /api/chat/message/ (use_function_calling: true)
    ↓
LLMFunctionCallingService
    ↓
OpenAI GPT-4 (analyzes intent)
    ↓
Calls appropriate Amadeus functions
    ↓
AmadeusService → Amadeus APIs
    ↓
Returns natural language response
```

## 🔗 Quick Links

- Amadeus Dashboard: https://developers.amadeus.com/my-apps
- OpenAI Dashboard: https://platform.openai.com/api-keys
- Amadeus Examples: https://github.com/amadeus4dev/amadeus-code-examples
- Amadeus Docs: https://developers.amadeus.com/self-service

## ✅ Health Check

```bash
# Check if APIs are configured
cd backend
python -c "from services.amadeus_service import AmadeusService; print('✓ Amadeus OK')"
python -c "from services.llm_function_calling import LLMFunctionCallingService; print('✓ OpenAI OK')"
```

---

**Need help?** See full documentation in `AMADEUS_INTEGRATION_README.md`
