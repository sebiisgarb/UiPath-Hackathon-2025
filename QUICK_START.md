# Backend Rebuild - Quick Start Guide

## 🎯 What Was Built

A complete Django backend for a travel chatbot using:
- **OpenRouter API** (Claude Sonnet 4) for intelligent conversation
- **Amadeus API** (15 tools) for real flight, hotel, and activity data
- **Tool-calling architecture** for dynamic API execution

## 📁 Project Structure

```
backend/
├── apps/
│   └── chat/                    # Single Django app
│       ├── views.py             # 2 endpoints: chat, reset
│       └── urls.py              # URL routing
├── services/
│   ├── chatbot_service.py       # Main orchestration (24KB)
│   ├── openrouter_service.py    # LLM client (3KB)
│   ├── amadeus_tool_service.py  # API wrappers (9KB)
│   └── amadeus_service.py       # Base Amadeus SDK
└── config/
    ├── settings.py              # Django config
    └── urls.py                  # Main routes

Root:
├── BACKEND_REBUILD_README.md    # Full documentation
├── REBUILD_CHANGES.md           # Detailed change log
├── test_backend.py              # Test script
└── example_usage.py             # Usage examples
```

## 🚀 Quick Start (3 Steps)

### 1. Set Environment Variables

Create `backend/.env`:
```bash
OPENROUTER_API_KEY=your-key-here
AMADEUS_CLIENT_ID=your-id-here
AMADEUS_CLIENT_SECRET=your-secret-here
AMADEUS_HOSTNAME=test
```

### 2. Start the Server

```bash
cd backend
python manage.py runserver
```

### 3. Test It

```bash
curl -X POST http://localhost:8000/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "Find flights from NYC to Paris"}'
```

## 🔧 API Endpoints

### POST /chat/
Send a message to the chatbot.

**Request:**
```json
{
  "message": "I want to travel to Paris next month",
  "sessionId": "optional-session-id"
}
```

**Response:**
```json
{
  "reply": "I'll help you plan your trip to Paris...",
  "state": {
    "origin_airport": null,
    "destination_airport": "CDG",
    "departure_date": "2025-12-15",
    "return_date": null,
    "adults": 1,
    "children": 0
  },
  "history": [...],
  "session_id": "uuid-here"
}
```

### POST /chat/reset/
Reset a session.

**Request:**
```json
{
  "sessionId": "session-id-to-reset"
}
```

## 🛠️ 15 Amadeus Tools Available

The LLM can automatically call these tools:

**Location & Airports:**
1. `airport_city_search` - Search for airports/cities
2. `airport_direct_destinations` - Get direct routes
3. `airline_destinations` - Get airline network

**Flights:**
4. `flight_offers_search` - Search flights
5. `flight_inspiration_search` - Get destination ideas
6. `flight_cheapest_date_search` - Find best prices
7. `flight_offers_price` - Confirm pricing
8. `trip_purpose_prediction` - Predict business/leisure

**Hotels:**
9. `hotel_list` - List hotels in city
10. `hotel_search` - Search hotel offers
11. `hotel_offers_by_hotel` - Get specific hotel
12. `hotel_ratings` - Get ratings/reviews

**Activities:**
13. `tours_and_activities` - Search by location
14. `tours_and_activities_by_square` - Search by area
15. `get_activity_details` - Get activity info

## 🎓 How It Works

```
User Message
    ↓
Chatbot Service
    ↓
OpenRouter (Claude) + Tool Definitions
    ↓
[If tool needed]
    ↓
Execute Amadeus API
    ↓
Return Results
    ↓
Claude Processes
    ↓
[Repeat if more tools needed]
    ↓
Final Answer to User
```

## ✅ Testing

Run the test script:
```bash
python test_backend.py
```

Expected output:
```
✅ All services imported successfully
✅ Django configuration valid
✅ URL routing configured correctly
✅ All 15 tools defined correctly
✅ Session management working
```

## 📝 Example Usage

Run the example script:
```bash
python example_usage.py
```

Or try these conversations:
- "Find flights from San Francisco to Tokyo in January"
- "Show me 5-star hotels in Rome"
- "What activities are near the Eiffel Tower?"
- "Find the cheapest dates to fly to Barcelona"

## 🔑 Getting API Keys

1. **OpenRouter**: https://openrouter.ai/
   - Sign up → Get API key → Add credits ($5 minimum)
   - Model used: `anthropic/claude-sonnet-4`

2. **Amadeus**: https://developers.amadeus.com/
   - Create account → Get test credentials (free)
   - Use test environment for development

## 📊 What Changed

**Before (Old Backend):**
- 3 Django apps (trips, chat, integrations)
- 10+ endpoints
- Mock data providers
- Step-by-step workflow
- Database-heavy

**After (New Backend):**
- 1 Django app (chat only)
- 2 endpoints (chat, reset)
- Real Amadeus APIs
- Dynamic tool-calling
- In-memory sessions

## 📚 Documentation Files

1. **BACKEND_REBUILD_README.md** - Complete technical documentation
2. **REBUILD_CHANGES.md** - Detailed change log
3. **test_backend.py** - Automated testing
4. **example_usage.py** - Usage examples
5. This file - Quick start guide

## 🐛 Troubleshooting

**"ModuleNotFoundError: No module named 'django'"**
```bash
pip install -r requirements.txt
```

**"OpenRouter API key not provided"**
```bash
# Create backend/.env with your API key
echo "OPENROUTER_API_KEY=your-key" >> backend/.env
```

**"Amadeus API credentials not provided"**
```bash
# Add to backend/.env
echo "AMADEUS_CLIENT_ID=your-id" >> backend/.env
echo "AMADEUS_CLIENT_SECRET=your-secret" >> backend/.env
```

**"Connection refused" when testing**
```bash
# Make sure server is running
cd backend && python manage.py runserver
```

## 🎯 Next Steps

1. ✅ Backend is built and tested
2. ⏳ Add your API keys to `.env`
3. ⏳ Test with real API calls
4. ⏳ Connect to frontend
5. ⏳ Add Redis for persistent sessions (optional)
6. ⏳ Add logging for debugging (optional)

## 💡 Tips

- Sessions are in-memory (lost on restart)
- Max 10 tool iterations per turn (prevents loops)
- Use test Amadeus environment for development
- OpenRouter charges per request (~$0.003 per chat turn)
- All tools use real Amadeus APIs (no mocks)

## 📞 Support

- Amadeus API docs: https://developers.amadeus.com/
- OpenRouter docs: https://openrouter.ai/docs
- Django docs: https://docs.djangoproject.com/

---

**Ready to test?**
```bash
cd backend && python manage.py runserver
```

Then in another terminal:
```bash
python example_usage.py
```
