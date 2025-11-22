# AI Trip Planner - Django Backend

A modular Django backend for an AI-powered trip planning application. This template includes three main apps: `trips`, `chat`, and `integrations`, along with service layers for LLM parsing, flight/hotel providers, and itinerary generation.

## Features

- **Modular Architecture**: Separate apps for trips, chat, and integrations
- **RESTful API**: Built with Django REST Framework
- **Mock Providers**: Flight and hotel mock data providers
- **LLM Parser**: Service to parse user messages and extract trip details
- **Itinerary Generator**: Automatic day-by-day itinerary creation
- **Admin Interface**: Full Django admin for managing data
- **API Documentation**: Clear endpoint documentation

## Project Structure

```
backend/
├── config/                 # Django project settings
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── trips/             # Trip planning app
│   │   ├── models.py      # TripRequest, FlightOption, HotelOption, ItineraryDay
│   │   ├── views.py       # API endpoints
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── admin.py
│   ├── chat/              # Chat interactions app
│   │   ├── models.py      # ChatSession, ChatMessage
│   │   ├── views.py
│   │   ├── serializers.py
│   │   └── urls.py
│   └── integrations/      # External service integrations
│       ├── models.py      # ExternalService, APILog
│       ├── views.py
│       ├── serializers.py
│       └── urls.py
├── services/              # Business logic layer
│   ├── llm_parser.py      # Parse user messages
│   ├── flight_provider.py # Generate flight options
│   ├── hotel_provider.py  # Generate hotel options
│   └── itinerary_generator.py # Generate itineraries
└── manage.py
```

## Installation

1. **Clone the repository**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r ../requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000`

## API Endpoints

### Trips App

#### POST /api/trips/plan/
Plan a complete trip from a user message.

**Request:**
```json
{
  "message": "I want to visit Paris next month for 5 days with my family"
}
```

**Response:**
```json
{
  "id": 1,
  "user_message": "I want to visit Paris next month for 5 days with my family",
  "destination": "Paris",
  "start_date": "2024-07-01",
  "end_date": "2024-07-06",
  "budget": null,
  "travelers_count": 1,
  "preferences": {},
  "status": "completed",
  "flight_options": [...],
  "hotel_options": [...],
  "itinerary_days": [...]
}
```

#### GET /api/trips/
List all trip requests.

#### GET /api/trips/{id}/
Get details of a specific trip.

### Chat App

#### POST /api/chat/message/
Send a message in a chat session.

**Request:**
```json
{
  "session_id": "optional-session-id",
  "message": "Hello, I need help planning a trip"
}
```

#### GET /api/chat/session/{session_id}/
Get a chat session with all messages.

#### GET /api/chat/sessions/
List all chat sessions.

### Integrations App

#### GET /api/integrations/services/
List all external service integrations.

#### POST /api/integrations/services/
Create a new external service integration.

#### GET /api/integrations/services/{id}/
Get details of a specific service.

#### GET /api/integrations/logs/
Get API logs for monitoring.

#### GET /api/integrations/health/
Check health status of all active services.

## Models

### Trips App

- **TripRequest**: Main model for trip planning requests
- **FlightOption**: Flight options for a trip
- **HotelOption**: Hotel options for a trip
- **ItineraryDay**: Daily itinerary entries

### Chat App

- **ChatSession**: Chat session container
- **ChatMessage**: Individual messages (user/assistant)

### Integrations App

- **ExternalService**: External API service configurations
- **APILog**: Logs of API calls for monitoring

## Services

### LLM Parser Service
Parses user messages to extract:
- Destination
- Travel dates
- Budget
- Number of travelers
- Preferences

### Flight Provider Service
Generates mock flight options with:
- Airlines and flight numbers
- Departure/arrival times
- Pricing
- Duration and stops

### Hotel Provider Service
Generates mock hotel options with:
- Hotel names and ratings
- Pricing per night
- Amenities
- Room types

### Itinerary Generator Service
Creates day-by-day itineraries with:
- Activities for each day
- Popular attractions
- Time schedules
- Descriptions

## Testing

Run tests with:
```bash
python manage.py test
```

Run specific app tests:
```bash
python manage.py test apps.trips
python manage.py test apps.chat
python manage.py test apps.integrations
```

## Admin Interface

Access the Django admin at `http://localhost:8000/admin/` to:
- View and manage trip requests
- Monitor chat sessions
- Configure external service integrations
- View API logs

## Development

### Adding New Features

1. **New Models**: Add to appropriate app's `models.py`
2. **New Endpoints**: Add views to `views.py` and URLs to `urls.py`
3. **New Services**: Add to `services/` directory
4. **Run Migrations**: After model changes
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

### Code Style

Follow PEP 8 guidelines. Use Django best practices.

## Production Deployment

1. Set `DEBUG=False` in `.env`
2. Configure proper `SECRET_KEY`
3. Set up PostgreSQL or another production database
4. Configure static files serving
5. Set up HTTPS
6. Configure CORS for your frontend domain
7. Add actual API keys for external services

## Future Enhancements

- Integrate real flight APIs (Amadeus, Skyscanner)
- Integrate real hotel APIs (Booking.com, Expedia)
- Add real LLM integration (OpenAI, Claude)
- Add user authentication
- Add payment processing
- Add booking confirmation
- Add email notifications
- Add real-time chat with WebSockets
- Add caching layer
- Add rate limiting

## License

This is a template project for the UiPath Hackathon 2025.
