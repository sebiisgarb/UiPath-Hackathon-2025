# Project Structure

```
UiPath-Hackathon-2025/
│
├── README.md                          # Main project documentation
├── requirements.txt                   # Python dependencies
├── .gitignore                        # Git ignore rules
├── quickstart.sh                     # Quick setup script
│
└── backend/                          # Django backend application
    │
    ├── manage.py                     # Django management script
    ├── .env.example                  # Environment variables template
    ├── README.md                     # Backend documentation
    ├── API_EXAMPLES.md              # API usage examples
    ├── ARCHITECTURE.md              # System architecture docs
    │
    ├── config/                       # Django project configuration
    │   ├── __init__.py
    │   ├── settings.py              # Django settings
    │   ├── urls.py                  # Main URL routing
    │   ├── wsgi.py                  # WSGI application
    │   └── asgi.py                  # ASGI application
    │
    ├── apps/                         # Django applications
    │   │
    │   ├── trips/                    # Trip planning app
    │   │   ├── __init__.py
    │   │   ├── apps.py              # App configuration
    │   │   ├── models.py            # Data models
    │   │   │   ├── TripRequest
    │   │   │   ├── FlightOption
    │   │   │   ├── HotelOption
    │   │   │   └── ItineraryDay
    │   │   ├── serializers.py       # DRF serializers
    │   │   ├── views.py             # API views
    │   │   │   ├── plan_trip()
    │   │   │   ├── list_trips()
    │   │   │   └── get_trip_detail()
    │   │   ├── urls.py              # URL routing
    │   │   ├── admin.py             # Admin interface
    │   │   ├── tests.py             # Unit tests
    │   │   └── migrations/          # Database migrations
    │   │       └── 0001_initial.py
    │   │
    │   ├── chat/                     # Chat interactions app
    │   │   ├── __init__.py
    │   │   ├── apps.py
    │   │   ├── models.py
    │   │   │   ├── ChatSession
    │   │   │   └── ChatMessage
    │   │   ├── serializers.py
    │   │   ├── views.py
    │   │   │   ├── send_message()
    │   │   │   ├── get_session()
    │   │   │   └── list_sessions()
    │   │   ├── urls.py
    │   │   ├── admin.py
    │   │   └── migrations/
    │   │       └── 0001_initial.py
    │   │
    │   └── integrations/            # External services app
    │       ├── __init__.py
    │       ├── apps.py
    │       ├── models.py
    │       │   ├── ExternalService
    │       │   └── APILog
    │       ├── serializers.py
    │       ├── views.py
    │       │   ├── services_list()
    │       │   ├── service_detail()
    │       │   ├── api_logs()
    │       │   └── service_health()
    │       ├── urls.py
    │       ├── admin.py
    │       └── migrations/
    │           └── 0001_initial.py
    │
    └── services/                     # Business logic layer
        ├── __init__.py
        ├── llm_parser.py            # Message parsing service
        │   └── LLMParserService
        │       └── parse_message()
        ├── flight_provider.py       # Flight data provider
        │   └── FlightProviderService
        │       └── get_flight_options()
        ├── hotel_provider.py        # Hotel data provider
        │   └── HotelProviderService
        │       └── get_hotel_options()
        └── itinerary_generator.py  # Itinerary generation
            └── ItineraryGeneratorService
                └── generate_itinerary()
```

## File Descriptions

### Root Level
- **README.md**: Main project overview and quick start guide
- **requirements.txt**: Python package dependencies (Django, DRF, etc.)
- **quickstart.sh**: Automated setup script for quick project initialization
- **.gitignore**: Specifies intentionally untracked files

### Backend Directory

#### Configuration Files
- **manage.py**: Django's command-line utility for administrative tasks
- **.env.example**: Template for environment variables (SECRET_KEY, DEBUG, etc.)
- **config/settings.py**: Django configuration (database, apps, middleware)
- **config/urls.py**: Root URL configuration mapping to app URLs
- **config/wsgi.py**: WSGI configuration for deployment
- **config/asgi.py**: ASGI configuration for async support

#### Apps

##### Trips App (Core)
- **models.py**: 
  - `TripRequest`: User's trip planning request
  - `FlightOption`: Available flight choices
  - `HotelOption`: Available hotel choices
  - `ItineraryDay`: Daily activity plans
  
- **views.py**:
  - `plan_trip()`: Main endpoint - creates complete trip plan
  - `list_trips()`: Lists all trip requests
  - `get_trip_detail()`: Retrieves specific trip details

- **serializers.py**: DRF serializers for JSON serialization/deserialization

##### Chat App
- **models.py**:
  - `ChatSession`: Container for conversation threads
  - `ChatMessage`: Individual messages with role (user/assistant)

- **views.py**:
  - `send_message()`: Handles chat message submission
  - `get_session()`: Retrieves chat history
  - `list_sessions()`: Lists all chat sessions

##### Integrations App
- **models.py**:
  - `ExternalService`: Configuration for external APIs
  - `APILog`: Logging for API calls and responses

- **views.py**:
  - `services_list()`: CRUD for service configurations
  - `api_logs()`: View API call logs
  - `service_health()`: Health check endpoint

#### Services Layer

##### LLM Parser Service
- Parses natural language trip requests
- Extracts: destination, dates, budget, travelers, preferences
- Currently uses regex patterns (production would use real LLM)

##### Flight Provider Service
- Generates mock flight options
- Configurable: airlines, routes, pricing, duration
- Ready for integration with real APIs (Amadeus, Skyscanner)

##### Hotel Provider Service
- Generates mock hotel options
- Configurable: chains, ratings, pricing, amenities
- Ready for integration with real APIs (Booking.com, Expedia)

##### Itinerary Generator Service
- Creates day-by-day activity plans
- City-specific attractions and activities
- Customizable based on travel style and preferences

## Database Tables

### trips_triprequest
Primary table for trip planning requests
- Fields: id, user_message, destination, dates, budget, travelers, preferences, status

### trips_flightoption
Flight options for each trip
- Fields: id, trip_request_id (FK), airline, flight details, price, stops

### trips_hoteloption
Hotel options for each trip
- Fields: id, trip_request_id (FK), hotel details, rating, price, amenities

### trips_itineraryday
Daily itinerary entries
- Fields: id, trip_request_id (FK), day_number, date, title, activities

### chat_chatsession
Chat conversation containers
- Fields: id, session_id, timestamps

### chat_chatmessage
Individual chat messages
- Fields: id, session_id (FK), role, content, metadata, timestamp

### integrations_externalservice
External service configurations
- Fields: id, name, service_type, api_key, endpoint, configuration

### integrations_apilog
API call logging
- Fields: id, service_id (FK), request/response data, timing, errors

## API Endpoints Summary

### Trips
- `POST /api/trips/plan/` - Create complete trip plan
- `GET /api/trips/` - List all trips
- `GET /api/trips/{id}/` - Get trip details

### Chat
- `POST /api/chat/message/` - Send chat message
- `GET /api/chat/session/{id}/` - Get chat session
- `GET /api/chat/sessions/` - List all sessions

### Integrations
- `GET /api/integrations/services/` - List services
- `POST /api/integrations/services/` - Create service
- `GET /api/integrations/services/{id}/` - Service details
- `PUT /api/integrations/services/{id}/` - Update service
- `DELETE /api/integrations/services/{id}/` - Delete service
- `GET /api/integrations/logs/` - View API logs
- `GET /api/integrations/health/` - Health check

## Testing Structure

### Trips App Tests (apps/trips/tests.py)
- `TripPlanningAPITest`: API endpoint tests
  - test_plan_trip_with_valid_message
  - test_plan_trip_without_message
  - test_plan_trip_generates_flight_options
  - test_plan_trip_generates_hotel_options
  - test_plan_trip_generates_itinerary
  - test_list_trips
  - test_get_trip_detail

- `TripModelTest`: Model tests
  - test_create_trip_request
  - test_create_flight_option

## Documentation Files

1. **README.md**: Project overview, installation, quick start
2. **API_EXAMPLES.md**: Detailed API usage with curl examples
3. **ARCHITECTURE.md**: System architecture and design decisions
4. **PROJECT_STRUCTURE.md**: This file - complete project layout

## Development Workflow

1. **Initial Setup**: Run `./quickstart.sh`
2. **Development**: 
   - Models: Define in `apps/*/models.py`
   - Business Logic: Add to `services/`
   - API Endpoints: Create in `apps/*/views.py`
   - Routes: Configure in `apps/*/urls.py`
3. **Testing**: Run `python manage.py test`
4. **Migrations**: `python manage.py makemigrations && python manage.py migrate`
5. **Admin**: Configure in `apps/*/admin.py`

## Key Features

✅ Modular architecture with separate apps
✅ RESTful API with Django REST Framework
✅ Comprehensive data models
✅ Service layer for business logic
✅ Mock data providers (ready for real API integration)
✅ Chat interface support
✅ External service integration framework
✅ Complete test coverage
✅ Admin interface
✅ Detailed documentation
