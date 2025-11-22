# Amadeus + LLM Function Calling Integration

This integration brings **real Amadeus travel APIs** and **OpenAI LLM function calling** to the application, replacing mock data with live travel information.

## 🎯 What's New

### 1. **Comprehensive Amadeus API Wrapper** (`services/amadeus_service.py`)
- **19 Functions** covering flights, hotels, activities, POIs, transfers, and more
- Based on official [Amadeus Code Examples](https://github.com/amadeus4dev/amadeus-code-examples)
- Easy-to-use Python interface
- Built-in error handling

### 2. **LLM Function Calling** (`services/llm_function_calling.py`)
- OpenAI GPT-4 powered intelligent function calling
- Automatically understands user intent
- Calls appropriate Amadeus functions
- Returns natural language responses

### 3. **Updated Chat System** (`apps/chat/views.py`)
- Chat endpoint now supports function calling
- Conversation history tracking
- Fallback to mock responses if APIs unavailable

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

New packages:
- `amadeus==8.1.0` - Official Amadeus Python SDK
- `openai==1.54.0` - OpenAI API for function calling

### 2. Get API Credentials

#### Amadeus API (Free for Testing!)
1. Go to https://developers.amadeus.com
2. Sign up for a free account
3. Create a new app (Self-Service)
4. Copy your **API Key** (Client ID) and **API Secret** (Client Secret)

#### OpenAI API
1. Go to https://platform.openai.com
2. Sign up or log in
3. Go to API Keys section
4. Create a new API key

### 3. Configure Environment Variables

Create/update `backend/.env`:

```bash
# OpenAI API
OPENAI_API_KEY=sk-...your-key-here

# Amadeus API
AMADEUS_CLIENT_ID=your-client-id
AMADEUS_CLIENT_SECRET=your-client-secret
AMADEUS_HOSTNAME=test  # Use 'test' for free tier
```

### 4. Test the Integration

```bash
cd backend
python manage.py runserver
```

Then test with curl:

```bash
# Test with LLM function calling
curl -X POST http://localhost:8000/api/chat/message/ \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Find me flights from New York to Paris on December 1st",
    "use_function_calling": true
  }'
```

## 📚 Available Functions

### Flight APIs
- ✈️ `search_flights` - Search flight offers
- 💰 `get_flight_cheapest_dates` - Find cheapest travel dates
- ⏰ `predict_flight_delay` - Predict flight delays

### Hotel APIs
- 🏨 `search_hotels_by_city` - Search hotels in a city
- 🏩 `search_hotels_by_hotels` - Get specific hotel offers
- ⭐ `get_hotel_ratings` - Get hotel sentiment ratings
- 🔍 `search_hotel_by_name` - Hotel name autocomplete

### Activities & POI APIs
- 🎭 `search_activities` - Find tours and activities
- 📍 `search_points_of_interest` - Find landmarks and attractions
- ℹ️ `get_activity_details` - Activity details
- 🏛️ `get_poi_details` - POI details

### Location APIs
- 🌍 `search_locations` - Search airports and cities
- ✈️ `search_airports` - Find nearby airports
- 📌 `get_location_details` - Location information

### Transfer APIs
- 🚗 `search_transfers` - Ground transportation options

### Recommendations
- 🎯 `get_travel_recommendations` - AI destination suggestions

### Airline & Airport Info
- ✈️ `lookup_airline` - Airline information
- 🛫 `get_airport_routes` - Airport routes

## 💡 Usage Examples

### Example 1: Direct Function Call

```python
from services.amadeus_service import AmadeusService

amadeus = AmadeusService()

# Search flights
result = amadeus.search_flights(
    origin='JFK',
    destination='CDG',
    departure_date='2025-12-01',
    adults=2,
    travel_class='ECONOMY'
)

if result['success']:
    flights = result['data']
    print(f"Found {len(flights)} flights")
```

### Example 2: LLM Function Calling

```python
from services.llm_function_calling import LLMFunctionCallingService

llm = LLMFunctionCallingService()

result = llm.chat_with_function_calling(
    user_message="Find me hotels in Paris for December 1-5, 2 guests"
)

print(result['response'])  # Natural language response
print(result['function_calls'])  # Functions called automatically
```

### Example 3: Chat API

```bash
curl -X POST http://localhost:8000/api/chat/message/ \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I need a complete trip to Rome: flights from NYC on Dec 10-17, hotel downtown, and show me the top attractions",
    "use_function_calling": true
  }'
```

The LLM will automatically:
1. Search for airport codes
2. Search for flights
3. Search for hotels
4. Search for points of interest
5. Synthesize everything into a coherent response

## 📖 Documentation

- **[AMADEUS_FUNCTIONS.md](AMADEUS_FUNCTIONS.md)** - Complete function reference
- **[USAGE_EXAMPLES.py](USAGE_EXAMPLES.py)** - Code examples
- **[API_EXAMPLES.md](API_EXAMPLES.md)** - API endpoint examples

## 🔄 Migrating from Mock Data

The application previously used mock data in:
- `flight_provider.py` - Now can use `AmadeusService.search_flights()`
- `hotel_provider.py` - Now can use `AmadeusService.search_hotels_by_city()`
- `itinerary_generator.py` - Can use `AmadeusService.search_activities()` and `search_points_of_interest()`

You can:
1. **Use real APIs when credentials available** - Best for production
2. **Keep mocks as fallback** - Good for development
3. **Gradually migrate** - Test with real APIs, fallback to mocks

## 🎨 Architecture

```
User Request
    ↓
Chat API (/api/chat/message/)
    ↓
LLMFunctionCallingService
    ↓
OpenAI GPT-4 (decides which functions to call)
    ↓
AmadeusService (executes API calls)
    ↓
Amadeus APIs (real travel data)
    ↓
Response to User
```

## 🔐 Security Notes

- Never commit API keys to version control
- Use environment variables for all credentials
- The `.env` file is in `.gitignore`
- Use `.env.example` as a template
- For production, use proper secret management

## 🐛 Troubleshooting

### "Amadeus API credentials not provided"
- Make sure `.env` file exists in `backend/` directory
- Check that `AMADEUS_CLIENT_ID` and `AMADEUS_CLIENT_SECRET` are set
- Restart the Django server after updating `.env`

### "OpenAI API key not provided"
- Set `OPENAI_API_KEY` in `.env`
- Get key from https://platform.openai.com
- Restart server

### "ResponseError" from Amadeus
- Check if your API credentials are correct
- Verify you're using the test environment for free tier
- Check API usage limits on Amadeus dashboard
- Verify IATA codes are correct (use `search_locations` to find them)

### Mock data still showing
- Set `use_function_calling: true` in API requests
- Check that both Amadeus and OpenAI credentials are configured
- Look at server logs for error messages

## 📊 API Limits

### Amadeus Free Tier (Test Environment)
- **Flights**: 2,000 calls/month
- **Hotels**: 2,000 calls/month
- **Activities**: Included
- **POIs**: Included
- Rate limit: 10 calls/second

### OpenAI API
- GPT-4 Turbo: $0.01 per 1K input tokens, $0.03 per 1K output tokens
- Function calling: Included in token pricing
- Rate limits: Based on your account tier

## 🔗 Resources

- **Amadeus for Developers**: https://developers.amadeus.com
- **Amadeus Code Examples**: https://github.com/amadeus4dev/amadeus-code-examples
- **Amadeus Python SDK**: https://github.com/amadeus4dev/amadeus-python
- **OpenAI Function Calling**: https://platform.openai.com/docs/guides/function-calling
- **Amadeus Community Discord**: https://discord.gg/cVrFBqx

## 🎉 What This Enables

With this integration, users can now:

1. **Natural Language Queries**: "Find me a cheap flight to Paris next week"
2. **Complex Multi-Step Planning**: "Plan a complete Rome trip with flights, hotel, and activities"
3. **Real-Time Data**: Live flight prices, hotel availability, actual attractions
4. **Intelligent Recommendations**: AI-powered destination suggestions
5. **Comprehensive Travel Search**: Flights, hotels, activities, transfers - all in one

## 🚧 Future Enhancements

Potential additions:
- [ ] Flight booking integration
- [ ] Hotel booking integration
- [ ] Payment processing
- [ ] User authentication and saved trips
- [ ] Email confirmations
- [ ] Calendar integration
- [ ] Price alerts
- [ ] Multi-language support

## 👥 Contributing

This integration is based on:
- Official Amadeus SDK and examples
- OpenAI function calling best practices
- Django REST framework patterns

For issues or improvements, please open a GitHub issue.

---

**Happy Travels! ✈️🌍**
