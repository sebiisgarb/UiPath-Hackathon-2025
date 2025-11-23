#!/usr/bin/env python3
"""
Example usage of the rebuilt travel chatbot backend.
Demonstrates how to interact with the /chat and /chat/reset endpoints.
"""

import requests
import json

# Backend URL
BASE_URL = "http://localhost:8000"

def chat(message, session_id=None):
    """Send a message to the chatbot."""
    url = f"{BASE_URL}/chat/"
    payload = {"message": message}
    
    if session_id:
        payload["sessionId"] = session_id
    
    response = requests.post(url, json=payload)
    return response.json()

def reset_session(session_id):
    """Reset a chat session."""
    url = f"{BASE_URL}/chat/reset/"
    payload = {"sessionId": session_id}
    
    response = requests.post(url, json=payload)
    return response.json()

def print_response(response):
    """Pretty print the chatbot response."""
    print("\n" + "=" * 60)
    print("🤖 CHATBOT RESPONSE:")
    print("=" * 60)
    print(f"\nReply: {response.get('reply', 'N/A')}")
    
    if 'state' in response:
        print("\n📊 State:")
        for key, value in response['state'].items():
            print(f"  - {key}: {value}")
    
    if 'session_id' in response:
        print(f"\n🔑 Session ID: {response['session_id']}")
    
    print("=" * 60)

def main():
    print("=" * 60)
    print("Travel Chatbot Backend - Usage Example")
    print("=" * 60)
    
    # Example 1: Start a conversation
    print("\n📝 Example 1: Starting a conversation")
    print("Message: 'I want to fly from New York to Paris next month'")
    
    try:
        response1 = chat("I want to fly from New York to Paris next month")
        print_response(response1)
        session_id = response1.get('session_id')
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to backend")
        print("   Make sure the server is running:")
        print("   cd backend && python manage.py runserver")
        return
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return
    
    # Example 2: Continue the conversation
    print("\n📝 Example 2: Continue conversation with same session")
    print("Message: 'I need tickets for 2 adults and return on the 22nd'")
    
    try:
        response2 = chat(
            "I need tickets for 2 adults and return on the 22nd",
            session_id=session_id
        )
        print_response(response2)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return
    
    # Example 3: Ask about hotels
    print("\n📝 Example 3: Ask about hotels in the same session")
    print("Message: 'Can you also find me hotels in Paris for those dates?'")
    
    try:
        response3 = chat(
            "Can you also find me hotels in Paris for those dates?",
            session_id=session_id
        )
        print_response(response3)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return
    
    # Example 4: Reset session
    print("\n📝 Example 4: Reset the session")
    
    try:
        reset_response = reset_session(session_id)
        print("\n" + "=" * 60)
        print("🔄 SESSION RESET:")
        print("=" * 60)
        print(f"Message: {reset_response.get('message', 'N/A')}")
        print("=" * 60)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return
    
    # Example 5: Start new conversation
    print("\n📝 Example 5: Start a new conversation")
    print("Message: 'What activities are there in Tokyo?'")
    
    try:
        response5 = chat("What activities are there in Tokyo?")
        print_response(response5)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return
    
    print("\n✅ Examples completed successfully!")
    print("\n📚 Additional examples:")
    print("  - 'Find the cheapest flights from London to Barcelona'")
    print("  - 'Show me 5-star hotels in Rome'")
    print("  - 'What are the direct destinations from JFK airport?'")
    print("  - 'Find activities near the Eiffel Tower'")
    print()

if __name__ == "__main__":
    main()
