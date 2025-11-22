# AI Trip Planner - Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         Client Layer                            │
│  (Frontend, Mobile App, API Consumers)                         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP/REST
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Django REST API                            │
│                    (Port 8000)                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                ┌─────────────┼─────────────┐
                │             │             │
                ▼             ▼             ▼
        ┌──────────┐  ┌──────────┐  ┌──────────────┐
        │  Trips   │  │   Chat   │  │ Integrations │
        │   App    │  │   App    │  │     App      │
        └──────────┘  └──────────┘  └──────────────┘
                │             │             │
                └─────────────┼─────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │ Services Layer  │
                    │                 │
                    │ • LLM Parser    │
                    │ • Flight Provider│
                    │ • Hotel Provider│
                    │ • Itinerary Gen │
                    └─────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │  Database       │
                    │  (SQLite/       │
                    │   PostgreSQL)   │
                    └─────────────────┘
```

## Application Structure

### 1. Trips App
**Purpose:** Core trip planning functionality

**Models:**
- `TripRequest`: Main trip request entity
  - user_message, destination, dates, budget, travelers
- `FlightOption`: Flight options for trips
  - airline, flight_number, times, price, stops
- `HotelOption`: Hotel options for trips
  - hotel_name, address, rating, price, amenities
- `ItineraryDay`: Daily itinerary entries
  - day_number, date, title, activities

**Endpoints:**
- `POST /api/trips/plan/` - Create trip plan
- `GET /api/trips/` - List trips
- `GET /api/trips/{id}/` - Get trip details

### 2. Chat App
**Purpose:** Conversational interface for trip planning

**Models:**
- `ChatSession`: Container for chat conversations
  - session_id, timestamps
- `ChatMessage`: Individual messages
  - role (user/assistant/system), content, metadata

**Endpoints:**
- `POST /api/chat/message/` - Send message
- `GET /api/chat/session/{id}/` - Get session
- `GET /api/chat/sessions/` - List sessions

### 3. Integrations App
**Purpose:** External service management

**Models:**
- `ExternalService`: Service configurations
  - name, service_type, api_key, endpoint
- `APILog`: API call logs
  - request/response data, timing, errors

**Endpoints:**
- `GET/POST /api/integrations/services/` - CRUD operations
- `GET /api/integrations/logs/` - View logs
- `GET /api/integrations/health/` - Health check

## Services Layer

### LLM Parser Service
**Responsibility:** Parse natural language messages

**Functions:**
- Extract destination
- Parse dates (relative and absolute)
- Identify budget
- Count travelers
- Extract preferences (luxury, family, adventure, etc.)

**Example Input:**
```
"I want to visit Paris next month for 5 days with my family"
```

**Example Output:**
```python
{
    'destination': 'Paris',
    'start_date': date(2025, 12, 22),
    'end_date': date(2025, 12, 27),
    'travelers_count': 1,
    'preferences': {'travel_style': 'family'}
}
```

### Flight Provider Service
**Responsibility:** Generate/fetch flight options

**Features:**
- Mock data generation (dev)
- Multiple airlines
- Various price points
- Different durations and stops
- Integration ready for real APIs

**Mock Airlines:**
- American, Delta, United, Southwest, JetBlue
- Lufthansa, British Airways, Air France, Emirates

### Hotel Provider Service
**Responsibility:** Generate/fetch hotel options

**Features:**
- Mock data generation (dev)
- Various hotel chains
- Rating-based pricing
- Amenity lists
- Room type options
- Integration ready for real APIs

**Mock Chains:**
- Hilton, Marriott, Hyatt, Sheraton
- Four Seasons, Ritz-Carlton, St. Regis

### Itinerary Generator Service
**Responsibility:** Create day-by-day plans

**Features:**
- City-specific attractions
- Activity timing
- Travel style adaptation
- Morning/afternoon/evening activities

**Supported Cities:**
- Paris, London, Rome, Tokyo, New York
- Generic templates for other cities

## Data Flow: Trip Planning

```
1. User sends message
   "I want to visit Paris for 5 days"
        │
        ▼
2. POST /api/trips/plan/
        │
        ▼
3. LLM Parser Service
   • Extracts: destination, dates, preferences
        │
        ▼
4. Create TripRequest in DB
        │
        ├─────────────┬─────────────┐
        ▼             ▼             ▼
5. Flight Provider  Hotel Provider  Itinerary Generator
   • 3-5 options    • 3-5 options   • Day-by-day plan
        │             │             │
        ▼             ▼             ▼
6. Save FlightOptions, HotelOptions, ItineraryDays
        │
        ▼
7. Return complete trip plan JSON
```

## Database Schema

### TripRequest
```sql
- id (PK)
- user_message (TEXT)
- destination (VARCHAR)
- start_date (DATE)
- end_date (DATE)
- budget (DECIMAL)
- travelers_count (INT)
- preferences (JSON)
- status (VARCHAR)
- created_at, updated_at
```

### FlightOption
```sql
- id (PK)
- trip_request_id (FK)
- airline (VARCHAR)
- flight_number (VARCHAR)
- departure_airport (VARCHAR)
- arrival_airport (VARCHAR)
- departure_time (DATETIME)
- arrival_time (DATETIME)
- price (DECIMAL)
- duration_minutes (INT)
- stops (INT)
- is_selected (BOOL)
```

### HotelOption
```sql
- id (PK)
- trip_request_id (FK)
- hotel_name (VARCHAR)
- address (TEXT)
- rating (DECIMAL)
- price_per_night (DECIMAL)
- total_price (DECIMAL)
- amenities (JSON)
- room_type (VARCHAR)
- is_selected (BOOL)
```

### ItineraryDay
```sql
- id (PK)
- trip_request_id (FK)
- day_number (INT)
- date (DATE)
- title (VARCHAR)
- description (TEXT)
- activities (JSON)
```

## Technology Stack

### Backend Framework
- **Django 5.0.1**: Web framework
- **Django REST Framework 3.14.0**: API framework
- **Python 3.12+**: Programming language

### Database
- **SQLite**: Development (default)
- **PostgreSQL**: Production (recommended)

### Additional Libraries
- **django-cors-headers**: CORS support
- **python-dotenv**: Environment variables

## Security Considerations

### Current (Development)
- Debug mode enabled
- SQLite database
- Simple secret key
- Local CORS only

### Production Recommendations
- [ ] Disable DEBUG
- [ ] Use strong SECRET_KEY
- [ ] Configure PostgreSQL
- [ ] Set up HTTPS
- [ ] Configure proper CORS
- [ ] Add rate limiting
- [ ] Implement authentication
- [ ] Encrypt API keys
- [ ] Set up logging
- [ ] Use environment-specific settings

## Scalability Considerations

### Current Limitations
- Synchronous processing
- Single server deployment
- In-memory/file-based database

### Future Enhancements
- [ ] Async task processing (Celery)
- [ ] Caching layer (Redis)
- [ ] Load balancing
- [ ] Database replication
- [ ] CDN for static files
- [ ] Microservices architecture
- [ ] Message queue (RabbitMQ/Kafka)
- [ ] Containerization (Docker)

## Testing Strategy

### Current Tests
- Model creation tests
- API endpoint tests
- Service layer tests

### Test Coverage
- Trips app: 9 tests
- All tests passing
- Unit tests for models
- Integration tests for API

### Future Testing
- [ ] Chat app tests
- [ ] Integrations app tests
- [ ] Service layer unit tests
- [ ] E2E tests
- [ ] Performance tests
- [ ] Load tests

## Deployment

### Local Development
```bash
./quickstart.sh
```

### Production Deployment
1. Set environment variables
2. Configure database
3. Run migrations
4. Collect static files
5. Use WSGI server (gunicorn/uWSGI)
6. Set up reverse proxy (nginx)
7. Configure SSL certificates
8. Set up monitoring

## API Versioning

### Current Version: v1 (implicit)
- No version in URL
- Consider adding `/api/v1/` prefix for future versions

### Future Versions
- `/api/v2/` for breaking changes
- Keep v1 supported during migration

## Monitoring & Logging

### Current
- Django debug logging
- Database queries logged
- Basic error handling

### Recommended
- [ ] Application monitoring (Sentry)
- [ ] Performance monitoring (New Relic)
- [ ] Log aggregation (ELK Stack)
- [ ] API analytics
- [ ] Uptime monitoring
- [ ] Error tracking

## Documentation

### Available Docs
- README.md - Project overview
- API_EXAMPLES.md - API usage examples
- ARCHITECTURE.md - This document
- Code comments - Inline documentation

### API Documentation Tools
- Consider adding: Swagger/OpenAPI
- Consider adding: Postman collection
