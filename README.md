# UiPath-Hackathon-2025

## AI Trip Planner - Django Backend Template

This repository contains a modular Django backend template for an AI-powered trip planning application, created for the UiPath Hackathon 2025.

### Features

- **Modular Architecture**: Three specialized apps (trips, chat, integrations)
- **Complete Models**: TripRequest, FlightOption, HotelOption, ItineraryDay, ChatSession, ChatMessage, ExternalService, APILog
- **Service Layer**: LLM Parser, Flight Provider, Hotel Provider, Itinerary Generator
- **RESTful API**: Full CRUD operations with Django REST Framework
- **Main Endpoint**: `POST /api/trips/plan/` - Parse message, generate options, create itinerary
- **Mock Providers**: Realistic mock data for flights and hotels
- **Admin Interface**: Complete Django admin for data management
- **Tests**: Comprehensive test suite

### Quick Start

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up the database**
   ```bash
   cd backend
   python manage.py migrate
   ```

3. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

4. **Run the server**
   ```bash
   python manage.py runserver
   ```

5. **Test the main endpoint**
   ```bash
   curl -X POST http://localhost:8000/api/trips/plan/ \
     -H "Content-Type: application/json" \
     -d '{"message": "I want to visit Paris next month for 5 days"}'
   ```

### Project Structure

```
├── backend/
│   ├── config/              # Django project settings
│   ├── apps/
│   │   ├── trips/          # Trip planning (main app)
│   │   ├── chat/           # Chat interactions
│   │   └── integrations/   # External service integrations
│   ├── services/           # Business logic layer
│   │   ├── llm_parser.py
│   │   ├── flight_provider.py
│   │   ├── hotel_provider.py
│   │   └── itinerary_generator.py
│   └── manage.py
└── requirements.txt
```

### API Endpoints

- `POST /api/trips/plan/` - Create complete trip plan from message
- `GET /api/trips/` - List all trips
- `GET /api/trips/{id}/` - Get trip details
- `POST /api/chat/message/` - Send chat message
- `GET /api/chat/sessions/` - List chat sessions
- `GET /api/integrations/services/` - Manage external services
- `GET /api/integrations/health/` - Check service health

### Documentation

See [backend/README.md](backend/README.md) for detailed documentation including:
- Complete API reference
- Model descriptions
- Service layer details
- Testing guide
- Deployment instructions

### Tech Stack

- Django 5.0.1
- Django REST Framework 3.14.0
- Python 3.12+
- SQLite (development) / PostgreSQL (production ready)

### License

Template project for UiPath Hackathon 2025