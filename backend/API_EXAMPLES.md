# API Examples

This document provides example API calls for all endpoints in the AI Trip Planner backend.

## Trips API

### 1. Plan a Complete Trip

**Endpoint:** `POST /api/trips/plan/`

**Description:** Creates a complete trip plan by parsing a user message and generating flight options, hotel options, and a day-by-day itinerary.

**Example Request:**
```bash
curl -X POST http://localhost:8000/api/trips/plan/ \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I want to visit Paris next month for 5 days with my family"
  }'
```

**Example Response:**
```json
{
  "id": 1,
  "user_message": "I want to visit Paris next month for 5 days with my family",
  "destination": "Paris",
  "start_date": "2025-12-22",
  "end_date": "2025-12-27",
  "budget": null,
  "travelers_count": 5,
  "preferences": {
    "travel_style": "family"
  },
  "status": "completed",
  "created_at": "2025-11-22T14:04:44.244804Z",
  "updated_at": "2025-11-22T14:04:44.254250Z",
  "flight_options": [
    {
      "id": 1,
      "airline": "Emirates",
      "flight_number": "DL458",
      "departure_airport": "EWR",
      "arrival_airport": "CDG",
      "departure_time": "2025-12-22T09:45:00Z",
      "arrival_time": "2025-12-22T20:53:00Z",
      "price": "2599.03",
      "currency": "USD",
      "duration_minutes": 668,
      "stops": 2,
      "is_selected": false
    }
  ],
  "hotel_options": [
    {
      "id": 1,
      "hotel_name": "Ritz-Carlton Paris Resort",
      "address": "374 Park Ave, Paris",
      "rating": "3.9",
      "price_per_night": "168.97",
      "currency": "USD",
      "total_price": "844.85",
      "amenities": ["Free WiFi", "Breakfast Included", "Pool"],
      "room_type": "Suite",
      "is_selected": false
    }
  ],
  "itinerary_days": [
    {
      "id": 1,
      "day_number": 1,
      "date": "2025-12-22",
      "title": "Arrival and Paris Introduction",
      "description": "Arrive in Paris, check into hotel...",
      "activities": [
        {
          "time": "09:00",
          "activity": "Arrive and check-in",
          "description": "Check into your accommodation",
          "duration": "2 hours"
        }
      ]
    }
  ]
}
```

**Other Example Messages:**
```bash
# Beach vacation
curl -X POST http://localhost:8000/api/trips/plan/ \
  -H "Content-Type: application/json" \
  -d '{"message": "Plan a luxury beach vacation to Dubai for 2 people"}'

# Mountain adventure
curl -X POST http://localhost:8000/api/trips/plan/ \
  -H "Content-Type: application/json" \
  -d '{"message": "I want to go hiking in the mountains of Tokyo next week"}'

# Budget trip
curl -X POST http://localhost:8000/api/trips/plan/ \
  -H "Content-Type: application/json" \
  -d '{"message": "Budget trip to Rome for 3 days"}'
```

### 2. List All Trips

**Endpoint:** `GET /api/trips/`

**Description:** Retrieves a list of all trip requests.

**Example Request:**
```bash
curl -X GET http://localhost:8000/api/trips/
```

### 3. Get Trip Details

**Endpoint:** `GET /api/trips/{id}/`

**Description:** Retrieves details of a specific trip by ID.

**Example Request:**
```bash
curl -X GET http://localhost:8000/api/trips/1/
```

## Chat API

### 1. Send a Chat Message

**Endpoint:** `POST /api/chat/message/`

**Description:** Sends a message in a chat session. Creates a new session if no session_id is provided.

**Example Request (New Session):**
```bash
curl -X POST http://localhost:8000/api/chat/message/ \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello, I need help planning a trip to Japan"
  }'
```

**Example Response:**
```json
{
  "id": 1,
  "session_id": "a688fff1-2261-46c1-afff-663a8185377e",
  "messages": [
    {
      "id": 1,
      "role": "user",
      "content": "Hello, I need help planning a trip to Japan",
      "metadata": {},
      "created_at": "2025-11-22T14:05:07.857794Z"
    },
    {
      "id": 2,
      "role": "assistant",
      "content": "I'd be happy to help you plan your trip!...",
      "metadata": {},
      "created_at": "2025-11-22T14:05:07.859344Z"
    }
  ],
  "created_at": "2025-11-22T14:05:07.855402Z",
  "updated_at": "2025-11-22T14:05:07.855455Z"
}
```

**Example Request (Existing Session):**
```bash
curl -X POST http://localhost:8000/api/chat/message/ \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "a688fff1-2261-46c1-afff-663a8185377e",
    "message": "I want to go in March"
  }'
```

### 2. Get Chat Session

**Endpoint:** `GET /api/chat/session/{session_id}/`

**Description:** Retrieves a chat session with all its messages.

**Example Request:**
```bash
curl -X GET http://localhost:8000/api/chat/session/a688fff1-2261-46c1-afff-663a8185377e/
```

### 3. List All Chat Sessions

**Endpoint:** `GET /api/chat/sessions/`

**Description:** Retrieves a list of all chat sessions.

**Example Request:**
```bash
curl -X GET http://localhost:8000/api/chat/sessions/
```

## Integrations API

### 1. List External Services

**Endpoint:** `GET /api/integrations/services/`

**Description:** Lists all configured external service integrations.

**Example Request:**
```bash
curl -X GET http://localhost:8000/api/integrations/services/
```

### 2. Create External Service

**Endpoint:** `POST /api/integrations/services/`

**Description:** Creates a new external service integration configuration.

**Example Request:**
```bash
curl -X POST http://localhost:8000/api/integrations/services/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Amadeus Flight API",
    "service_type": "flight",
    "api_key": "your-api-key-here",
    "api_endpoint": "https://api.amadeus.com/v2",
    "is_active": true,
    "configuration": {
      "timeout": 30,
      "retry_count": 3
    }
  }'
```

### 3. Get Service Details

**Endpoint:** `GET /api/integrations/services/{id}/`

**Description:** Retrieves details of a specific external service.

**Example Request:**
```bash
curl -X GET http://localhost:8000/api/integrations/services/1/
```

### 4. Update Service

**Endpoint:** `PUT /api/integrations/services/{id}/`

**Description:** Updates an external service configuration.

**Example Request:**
```bash
curl -X PUT http://localhost:8000/api/integrations/services/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "is_active": false
  }'
```

### 5. Delete Service

**Endpoint:** `DELETE /api/integrations/services/{id}/`

**Description:** Deletes an external service configuration.

**Example Request:**
```bash
curl -X DELETE http://localhost:8000/api/integrations/services/1/
```

### 6. Get API Logs

**Endpoint:** `GET /api/integrations/logs/`

**Description:** Retrieves API logs for monitoring and debugging.

**Example Request:**
```bash
# Get all logs (limited to 100 recent)
curl -X GET http://localhost:8000/api/integrations/logs/

# Filter by service
curl -X GET 'http://localhost:8000/api/integrations/logs/?service_id=1'

# Limit results
curl -X GET 'http://localhost:8000/api/integrations/logs/?limit=50'
```

### 7. Check Service Health

**Endpoint:** `GET /api/integrations/health/`

**Description:** Checks the health status of all active services.

**Example Request:**
```bash
curl -X GET http://localhost:8000/api/integrations/health/
```

**Example Response:**
```json
{
  "status": "ok",
  "services": [
    {
      "service": "Amadeus Flight API",
      "type": "flight",
      "status": "healthy",
      "endpoint": "https://api.amadeus.com/v2"
    }
  ]
}
```

## Testing with Python Requests

You can also use Python's `requests` library:

```python
import requests
import json

# Plan a trip
response = requests.post(
    'http://localhost:8000/api/trips/plan/',
    json={'message': 'I want to visit Paris next month for 5 days'}
)
trip_data = response.json()
print(f"Trip ID: {trip_data['id']}")
print(f"Destination: {trip_data['destination']}")
print(f"Flight options: {len(trip_data['flight_options'])}")

# Start a chat session
response = requests.post(
    'http://localhost:8000/api/chat/message/',
    json={'message': 'Hello, help me plan a trip'}
)
chat_data = response.json()
session_id = chat_data['session_id']
print(f"Session ID: {session_id}")

# Continue the chat
response = requests.post(
    'http://localhost:8000/api/chat/message/',
    json={
        'session_id': session_id,
        'message': 'I want to go to Tokyo'
    }
)
```

## Error Responses

### 400 Bad Request
```json
{
  "message": ["This field is required."]
}
```

### 404 Not Found
```json
{
  "error": "Trip not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "Failed to create trip plan",
  "detail": "Specific error message"
}
```
