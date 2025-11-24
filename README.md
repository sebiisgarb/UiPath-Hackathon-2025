SkyPath: AI-Powered Travel Assistant

Proudly awarded 4th place at the UiPath Future Forward Hackathon 2025!

Overview:
SkyPath is an AI-powered travel assistant designed to streamline the entire trip-planning experience. Instead of dealing with chaotic aggregators and irrelevant options, SkyPath uses specialized AI agents connected directly to real Amadeus data to deliver accurate and personalized travel plans.

Key Features:
1. Flight Optimization Engine:
   - Refines schedules, budgets, layovers, luggage rules, and travel constraints.
   - No hallucinations: uses clean, real Amadeus data.

2. Hotel Recommendations:
   - Suggests accommodations based on location, price, preferences, and style.
   - Powered by Amadeus hotel datasets.

3. Custom Itinerary Generator:
   - Builds tailored day-by-day itineraries using user interests, time optimization, context, and local activity data.

4. Multi-Agent AI System:
   - Smart agents collaborate to enhance accuracy, filtering, and relevance throughout the planning flow.

Tech Stack:
Backend: Django (Python)
- Multi-agent orchestration layer
- Amadeus API integration
- Business logic for flight, hotel, and itinerary agents

Frontend: React
- User interface for travel planning
- Displays optimized flights, hotels, and itineraries

AI:
- Large Language Models coordinated through specialized agents
- Data validation, context sharing, and filtering


Project Structure (Generic):
/backend (Django)
  /sky_path
  /agents
  /services
  /utils
  manage.py

/frontend (React)
  /src
  /public

requirements.txt
README.txt

Architecture Summary:
- Orchestrator Agent receives user requests.
- Delegates tasks to:
  * Flight Agent
  * Hotel Agent
  * Itinerary Agent
- Agents fetch and validate real-time Amadeus data.
- Orchestrator compiles a final, coherent travel plan.

Future Enhancements:
- Multi-city route generation
- Local transport recommendations
- Google Maps integration
- Full UiPath automation pipelines

Credits:
Team Skepya — Hackathon project created with passion and innovation.

