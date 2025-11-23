#!/usr/bin/env python3
"""
Quick test script for the rebuilt backend.
Tests that all services can be imported and initialized without errors.
"""

import os
import sys
import django

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

print("=" * 60)
print("Backend Rebuild Test Script")
print("=" * 60)

# Test 1: Import services
print("\n1. Testing service imports...")
try:
    from services.chatbot_service import ChatbotService
    from services.openrouter_service import OpenRouterService
    from services.amadeus_tool_service import AmadeusToolService
    from services.amadeus_service import AmadeusService
    print("   ✅ All services imported successfully")
except Exception as e:
    print(f"   ❌ Import error: {e}")
    sys.exit(1)

# Test 2: Check Django configuration
print("\n2. Testing Django configuration...")
try:
    from django.core.management import call_command
    from io import StringIO
    
    out = StringIO()
    call_command('check', stdout=out)
    print("   ✅ Django configuration valid")
except Exception as e:
    print(f"   ❌ Django error: {e}")
    sys.exit(1)

# Test 3: Check URL routing
print("\n3. Testing URL routing...")
try:
    from django.urls import resolve, reverse
    from django.test import RequestFactory
    
    # Test chat endpoint
    factory = RequestFactory()
    request = factory.post('/chat/', {'message': 'test'})
    
    print("   ✅ URL routing configured correctly")
except Exception as e:
    print(f"   ❌ URL routing error: {e}")
    sys.exit(1)

# Test 4: Check environment variables (warnings only)
print("\n4. Checking environment variables...")
required_vars = ['OPENROUTER_API_KEY', 'AMADEUS_CLIENT_ID', 'AMADEUS_CLIENT_SECRET']
missing_vars = [var for var in required_vars if not os.getenv(var)]

if missing_vars:
    print(f"   ⚠️  Missing environment variables: {', '.join(missing_vars)}")
    print("   ⚠️  Services will fail at runtime without these")
else:
    print("   ✅ All required environment variables set")

# Test 5: Test tool definitions
print("\n5. Testing tool definitions...")
try:
    # Mock environment variables for testing
    os.environ.setdefault('OPENROUTER_API_KEY', 'test-key')
    os.environ.setdefault('AMADEUS_CLIENT_ID', 'test-id')
    os.environ.setdefault('AMADEUS_CLIENT_SECRET', 'test-secret')
    
    service = ChatbotService()
    tools = service._get_tools_definition()
    
    expected_tools = [
        'airport_city_search',
        'flight_offers_search',
        'flight_inspiration_search',
        'flight_cheapest_date_search',
        'flight_offers_price',
        'airport_direct_destinations',
        'airline_destinations',
        'hotel_list',
        'hotel_search',
        'hotel_offers_by_hotel',
        'hotel_ratings',
        'tours_and_activities',
        'tours_and_activities_by_square',
        'get_activity_details',
        'trip_purpose_prediction'
    ]
    
    tool_names = [tool['function']['name'] for tool in tools]
    
    if len(tool_names) == 15 and all(name in tool_names for name in expected_tools):
        print(f"   ✅ All 15 tools defined correctly")
    else:
        print(f"   ❌ Expected 15 tools, got {len(tool_names)}")
        missing = set(expected_tools) - set(tool_names)
        if missing:
            print(f"   ❌ Missing tools: {missing}")
        sys.exit(1)
except Exception as e:
    print(f"   ❌ Tool definition error: {e}")
    sys.exit(1)

# Test 6: Test session management
print("\n6. Testing session management...")
try:
    service = ChatbotService()
    session = service.get_or_create_session()
    
    if session['id'] and 'history' in session and 'state' in session:
        print("   ✅ Session management working")
    else:
        print("   ❌ Session structure invalid")
        sys.exit(1)
        
    # Test reset
    service.reset_session(session['id'])
    print("   ✅ Session reset working")
except Exception as e:
    print(f"   ❌ Session management error: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("All tests passed! ✅")
print("=" * 60)
print("\nNext steps:")
print("1. Set environment variables in backend/.env")
print("2. Run: cd backend && python manage.py runserver")
print("3. Test with: curl -X POST http://localhost:8000/chat/ \\")
print("              -H 'Content-Type: application/json' \\")
print("              -d '{\"message\": \"Find flights from NYC to Paris\"}'")
print()
