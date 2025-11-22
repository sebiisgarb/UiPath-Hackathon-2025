# Travel Planning Workflow with Claude Sonnet 4.5

This document explains the new travel planning workflow that uses Claude Sonnet 4.5 via OpenRouter to guide users through a structured conversation to collect travel information.

## Overview

The system now uses a **sequential workflow** to collect travel information:

1. **Destination** - Where to travel
2. **Travel Dates** - When to travel (departure & return)
3. **Flight Preferences** - Flight class, airline, etc.
4. **Hotel Preferences** - Star rating, hotel name, etc.

Each step must be completed before moving to the next. The system provides **real-time feedback** with checkmarks showing what's been collected.

## Key Changes from Previous Version

### Before (OpenAI Function Calling)
- Used OpenAI GPT-4 with function calling
- Called Amadeus APIs directly in conversation
- Less structured workflow

### After (Claude Sonnet 4.5 Workflow)
- Uses Claude Sonnet 4.5 via OpenRouter
- Structured sequential workflow with progress tracking
- Extracts information from natural language
- Provides frontend-friendly responses with status checks
- Only proceeds when current step is complete

## Setup

### 1. Get OpenRouter API Key

1. Go to https://openrouter.ai/
2. Sign up or log in
3. Go to **Keys** section
4. Create a new API key
5. Copy your API key

### 2. Configure Environment Variables

Edit `backend/.env`:

```bash
# OpenRouter API (for Claude Sonnet 4.5)
OPENROUTER_API_KEY=your-openrouter-api-key-here

# Amadeus API (optional - for real travel data)
AMADEUS_CLIENT_ID=your-amadeus-client-id
AMADEUS_CLIENT_SECRET=your-amadeus-client-secret
AMADEUS_HOSTNAME=test
```

### 3. Run Database Migration

```bash
cd backend
python manage.py migrate
```

### 4. Start the Server

```bash
python manage.py runserver
```

## API Usage

### Endpoint

```
POST /api/chat/message/
```

### Request Format

```json
{
  "session_id": "optional-session-id",
  "message": "I want to visit Paris"
}
```

- `session_id` (optional): If not provided, a new session is created
- `message` (required): User's natural language message

### Response Format

```json
{
  "session_id": "uuid-of-session",
  "message": "Great! You're going to Paris. When would you like to travel?",
  "workflow": {
    "current_step": "travel_dates",
    "is_complete": false,
    "progress": {
      "destination": {
        "completed": true,
        "label": "Destination",
        "data": {
          "city": "Paris"
        }
      },
      "travel_dates": {
        "completed": false,
        "label": "Travel Dates",
        "data": null
      },
      "flight": {
        "completed": false,
        "label": "Flight Preferences",
        "data": null
      },
      "hotel": {
        "completed": false,
        "label": "Hotel Preferences",
        "data": null
      }
    }
  },
  "collected_info": {
    "destination": {
      "city": "Paris"
    },
    "travel_dates": null,
    "flight": null,
    "hotel": null
  },
  "extracted_from_message": {
    "destination": {
      "city": "Paris"
    }
  },
  "messages": [
    {
      "role": "user",
      "content": "I want to visit Paris",
      "created_at": "2025-11-22T22:00:00Z"
    },
    {
      "role": "assistant",
      "content": "Great! You're going to Paris. When would you like to travel?",
      "created_at": "2025-11-22T22:00:01Z"
    }
  ]
}
```

## Workflow Example

### Step 1: Destination

**User:** "I want to plan a trip"

**Response:**
```json
{
  "message": "Where would you like to travel? Please tell me your destination city.",
  "workflow": {
    "current_step": "destination",
    "is_complete": false,
    "progress": {
      "destination": {"completed": false},
      "travel_dates": {"completed": false},
      "flight": {"completed": false},
      "hotel": {"completed": false}
    }
  }
}
```

**User:** "I want to go to Paris"

**Response:**
```json
{
  "message": "Great! You're going to Paris. When would you like to travel?",
  "workflow": {
    "current_step": "travel_dates",
    "is_complete": false,
    "progress": {
      "destination": {
        "completed": true,
        "data": {"city": "Paris"}
      },
      "travel_dates": {"completed": false},
      "flight": {"completed": false},
      "hotel": {"completed": false}
    }
  }
}
```

### Step 2: Travel Dates

**User:** "Next month for a week"

**Response:**
```json
{
  "message": "Excellent! Now let's find you a flight. Do you have any preferences?",
  "workflow": {
    "current_step": "flight",
    "is_complete": false,
    "progress": {
      "destination": {"completed": true},
      "travel_dates": {
        "completed": true,
        "data": {
          "departure_date": "2025-12-22",
          "return_date": "2025-12-29",
          "duration_days": 7
        }
      },
      "flight": {"completed": false},
      "hotel": {"completed": false}
    }
  }
}
```

### Step 3: Flight Preferences

**User:** "Business class please"

**Response:**
```json
{
  "message": "Almost done! Do you have any preferences for your hotel?",
  "workflow": {
    "current_step": "hotel",
    "is_complete": false,
    "progress": {
      "destination": {"completed": true},
      "travel_dates": {"completed": true},
      "flight": {
        "completed": true,
        "data": {"class": "business"}
      },
      "hotel": {"completed": false}
    }
  }
}
```

### Step 4: Hotel Preferences

**User:** "4 or 5 star hotel"

**Response:**
```json
{
  "message": "Perfect! I have all the information I need:\n\n✓ Destination: Paris\n✓ Travel Dates: 2025-12-22 to 2025-12-29 (7 days)\n✓ Flight: business class\n✓ Hotel: 4-star\n\nWould you like me to search for flights and hotels now?",
  "workflow": {
    "current_step": null,
    "is_complete": true,
    "progress": {
      "destination": {"completed": true},
      "travel_dates": {"completed": true},
      "flight": {"completed": true},
      "hotel": {
        "completed": true,
        "data": {"star_rating": 4}
      }
    }
  }
}
```

## Frontend Integration Guide

### Displaying Progress

Use the `workflow.progress` object to show checkmarks:

```jsx
const ProgressIndicator = ({ workflow }) => {
  const steps = [
    { key: 'destination', icon: '📍' },
    { key: 'travel_dates', icon: '📅' },
    { key: 'flight', icon: '✈️' },
    { key: 'hotel', icon: '🏨' }
  ];
  
  return (
    <div className="progress-steps">
      {steps.map(step => (
        <div key={step.key} className={workflow.progress[step.key].completed ? 'completed' : 'pending'}>
          <span className="icon">{step.icon}</span>
          <span className="label">{workflow.progress[step.key].label}</span>
          {workflow.progress[step.key].completed && <span className="check">✓</span>}
        </div>
      ))}
    </div>
  );
};
```

### Handling Messages

```javascript
const sendMessage = async (message, sessionId = null) => {
  const response = await fetch('/api/chat/message/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      message: message,
      session_id: sessionId
    })
  });
  
  const data = await response.json();
  
  // Update UI with:
  // - data.message (assistant's response)
  // - data.workflow.progress (progress indicators)
  // - data.workflow.is_complete (enable search button when true)
  
  return data;
};
```

### Complete Example

```javascript
import React, { useState } from 'react';

function TravelPlanner() {
  const [sessionId, setSessionId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [workflow, setWorkflow] = useState(null);
  const [input, setInput] = useState('');
  
  const sendMessage = async () => {
    if (!input.trim()) return;
    
    const response = await fetch('/api/chat/message/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: input,
        session_id: sessionId
      })
    });
    
    const data = await response.json();
    
    setSessionId(data.session_id);
    setMessages(data.messages);
    setWorkflow(data.workflow);
    setInput('');
  };
  
  return (
    <div className="travel-planner">
      {/* Progress Indicator */}
      {workflow && (
        <div className="progress-bar">
          {Object.entries(workflow.progress).map(([key, status]) => (
            <div key={key} className={status.completed ? 'step-completed' : 'step-pending'}>
              {status.label} {status.completed && '✓'}
            </div>
          ))}
        </div>
      )}
      
      {/* Messages */}
      <div className="messages">
        {messages.map((msg, i) => (
          <div key={i} className={`message ${msg.role}`}>
            {msg.content}
          </div>
        ))}
      </div>
      
      {/* Input */}
      <div className="input-area">
        <input 
          value={input} 
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
          placeholder="Type your message..."
        />
        <button onClick={sendMessage}>Send</button>
        
        {workflow?.is_complete && (
          <button className="search-btn" onClick={handleSearch}>
            Search Flights & Hotels
          </button>
        )}
      </div>
    </div>
  );
}
```

## Natural Language Examples

The system can extract information from various natural language inputs:

### Destination
- "I want to go to Paris"
- "Planning a trip to Tokyo"
- "Visit Rome"

### Travel Dates
- "Next week"
- "December 1st to December 15th"
- "In January for 5 days"
- "From March 10 to March 20"

### Flight Preferences
- "Business class"
- "Direct flight only"
- "Prefer American Airlines"
- "Cheapest option"

### Hotel Preferences
- "5 star hotel"
- "Luxury accommodation"
- "Budget hotel"
- "Marriott or Hilton"

## Testing

### Test the API

```bash
# Start conversation
curl -X POST http://localhost:8000/api/chat/message/ \
  -H "Content-Type: application/json" \
  -d '{"message": "I want to plan a trip"}'

# Continue with session_id from response
curl -X POST http://localhost:8000/api/chat/message/ \
  -H "Content-Type: application/json" \
  -d '{"session_id": "your-session-id", "message": "I want to go to Paris"}'

# Add travel dates
curl -X POST http://localhost:8000/api/chat/message/ \
  -H "Content-Type: application/json" \
  -d '{"session_id": "your-session-id", "message": "Next month for a week"}'

# Add flight preference
curl -X POST http://localhost:8000/api/chat/message/ \
  -H "Content-Type: application/json" \
  -d '{"session_id": "your-session-id", "message": "Business class"}'

# Add hotel preference
curl -X POST http://localhost:8000/api/chat/message/ \
  -H "Content-Type: application/json" \
  -d '{"session_id": "your-session-id", "message": "5 star hotel"}'
```

## Architecture

```
User Message
    ↓
Django API (/api/chat/message/)
    ↓
TravelPlanningService
    ↓
Claude Sonnet 4.5 (via OpenRouter)
    ↓
Extracts: destination, dates, flight, hotel
    ↓
Determines next question based on workflow
    ↓
Returns structured response with progress
    ↓
Response to Frontend
```

## Benefits

1. **Structured Flow**: Clear progression through travel planning steps
2. **Progress Tracking**: Visual feedback with checkmarks for each step
3. **Flexible Input**: Accepts natural language, extracts structured data
4. **Session Management**: Maintains state across conversation
5. **Frontend-Friendly**: Clean JSON response format with all needed data
6. **Claude Sonnet 4.5**: State-of-the-art LLM for better understanding
7. **OpenRouter**: Flexible API access to multiple LLM providers

## Troubleshooting

### "OpenRouter API key not provided"
- Make sure `OPENROUTER_API_KEY` is set in `backend/.env`
- Restart the Django server after adding the key

### Information not extracted correctly
- The system uses Claude for extraction but has fallback patterns
- Check the `extracted_from_message` field to see what was extracted
- Make sure your input is clear and includes the information

### Session not persisting
- Make sure you're passing `session_id` in subsequent requests
- Session data is stored in the database

## Future Enhancements

- Integration with Amadeus APIs when workflow is complete
- Ability to modify previously entered information
- Support for more complex travel scenarios (multi-city, etc.)
- Booking confirmation workflow
- Payment processing

## Resources

- OpenRouter: https://openrouter.ai/
- Claude Sonnet 4.5: https://www.anthropic.com/claude
- Amadeus APIs: https://developers.amadeus.com
