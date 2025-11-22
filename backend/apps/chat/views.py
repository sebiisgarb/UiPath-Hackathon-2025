import uuid
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import ChatSession, ChatMessage
from .serializers import (
    ChatSessionSerializer,
    ChatMessageSerializer,
    ChatRequestSerializer
)


@api_view(['POST'])
def send_message(request):
    """
    Send a message in a chat session.
    
    POST /api/chat/message/
    
    Request body:
    {
        "session_id": "optional-existing-session-id",
        "message": "User's message"
    }
    """
    serializer = ChatRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    session_id = serializer.validated_data.get('session_id')
    message_content = serializer.validated_data['message']
    
    # Get or create chat session
    if session_id:
        try:
            chat_session = ChatSession.objects.get(session_id=session_id)
        except ChatSession.DoesNotExist:
            return Response(
                {'error': 'Chat session not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    else:
        # Create new session
        session_id = str(uuid.uuid4())
        chat_session = ChatSession.objects.create(session_id=session_id)
    
    # Save user message
    user_message = ChatMessage.objects.create(
        session=chat_session,
        role='user',
        content=message_content
    )
    
    # Generate assistant response (mock response)
    assistant_response = _generate_response(message_content)
    
    assistant_message = ChatMessage.objects.create(
        session=chat_session,
        role='assistant',
        content=assistant_response
    )
    
    # Return the session with messages
    session_serializer = ChatSessionSerializer(chat_session)
    return Response(session_serializer.data)


@api_view(['GET'])
def get_session(request, session_id):
    """
    Get a chat session with all messages.
    
    GET /api/chat/session/{session_id}/
    """
    try:
        chat_session = ChatSession.objects.get(session_id=session_id)
        serializer = ChatSessionSerializer(chat_session)
        return Response(serializer.data)
    except ChatSession.DoesNotExist:
        return Response(
            {'error': 'Chat session not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
def list_sessions(request):
    """
    List all chat sessions.
    
    GET /api/chat/sessions/
    """
    sessions = ChatSession.objects.all()
    serializer = ChatSessionSerializer(sessions, many=True)
    return Response(serializer.data)


def _generate_response(user_message: str) -> str:
    """
    Generate a mock assistant response.
    In production, this would call an LLM API.
    """
    message_lower = user_message.lower()
    
    if any(word in message_lower for word in ['trip', 'travel', 'vacation', 'visit']):
        return ("I'd be happy to help you plan your trip! To create the best itinerary for you, "
                "could you provide more details about:\n"
                "- Your destination\n"
                "- Travel dates or preferred time of year\n"
                "- Budget range\n"
                "- Number of travelers\n"
                "- Any specific interests or preferences")
    elif any(word in message_lower for word in ['flight', 'fly']):
        return ("I can help you find flight options. Please provide:\n"
                "- Departure city\n"
                "- Destination\n"
                "- Travel dates\n"
                "- Number of passengers\n"
                "- Preferred airline or class")
    elif any(word in message_lower for word in ['hotel', 'accommodation', 'stay']):
        return ("I can help you find accommodation. Please share:\n"
                "- Destination\n"
                "- Check-in and check-out dates\n"
                "- Number of guests\n"
                "- Preferred star rating or budget\n"
                "- Any specific amenities you need")
    else:
        return ("Hello! I'm your AI trip planning assistant. I can help you:\n"
                "- Plan complete trips with flights, hotels, and itineraries\n"
                "- Find flight options\n"
                "- Search for accommodations\n"
                "- Create day-by-day itineraries\n\n"
                "How can I assist you with your travel plans today?")
