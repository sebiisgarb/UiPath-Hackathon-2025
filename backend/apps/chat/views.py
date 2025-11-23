import uuid
import json
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import ChatSession, ChatMessage
from .serializers import (
    ChatSessionSerializer,
    ChatMessageSerializer,
    ChatRequestSerializer
)
from services.travel_planning_service import TravelPlanningService
from services.openrouter_function_calling import OpenRouterFunctionCallingService


@api_view(['POST'])
def send_message(request):
    """
    Send a message in a chat session with travel planning workflow.
    
    POST /api/chat/message/
    
    Request body:
    {
        "session_id": "optional-existing-session-id",
        "message": "User's message"
    }
    
    Response includes:
    - message: Next question or response
    - workflow: Current workflow state with progress checkmarks
    - collected_info: All travel information collected so far
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
        chat_session = ChatSession.objects.create(
            session_id=session_id,
            workflow_state={}
        )
    
    # Save user message
    user_message = ChatMessage.objects.create(
        session=chat_session,
        role='user',
        content=message_content
    )
    
    # Process with travel planning service
    try:
        # Initialize travel planning service
        travel_service = TravelPlanningService()
        
        # Get current workflow state from session
        current_state = chat_session.workflow_state or {}
        
        # Extract information and get next question
        result = travel_service.extract_travel_info(
            message=message_content,
            current_state=current_state
        )
        
        # Update session workflow state
        chat_session.workflow_state = result['collected_info']
        chat_session.save()
        
        # Format response for frontend
        formatted_response = travel_service.format_response_for_frontend(
            result=result,
            user_message=message_content
        )
        
        # Create assistant response message
        assistant_response = formatted_response['message']
        
        # Store the full response in metadata
        assistant_message = ChatMessage.objects.create(
            session=chat_session,
            role='assistant',
            content=assistant_response,
            metadata=formatted_response
        )
        
        # Return formatted response with session info
        return Response({
            'session_id': session_id,
            'message': assistant_response,
            'workflow': formatted_response['workflow'],
            'collected_info': formatted_response['collected_info'],
            'extracted_from_message': formatted_response.get('extracted_from_message', {}),
            'messages': [
                {
                    'role': user_message.role,
                    'content': user_message.content,
                    'created_at': user_message.created_at.isoformat()
                },
                {
                    'role': assistant_message.role,
                    'content': assistant_message.content,
                    'created_at': assistant_message.created_at.isoformat()
                }
            ]
        })
        
    except ValueError as e:
        # API key not configured
        error_message = str(e)
        if 'OpenRouter' in error_message:
            error_message = "Travel planning service is not configured. Please set OPENROUTER_API_KEY environment variable."
        
        # Create fallback response
        assistant_message = ChatMessage.objects.create(
            session=chat_session,
            role='assistant',
            content=error_message
        )
        
        return Response({
            'session_id': session_id,
            'message': error_message,
            'error': True,
            'messages': [
                {
                    'role': user_message.role,
                    'content': user_message.content,
                    'created_at': user_message.created_at.isoformat()
                },
                {
                    'role': assistant_message.role,
                    'content': assistant_message.content,
                    'created_at': assistant_message.created_at.isoformat()
                }
            ]
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        # Unexpected error
        error_message = f"I apologize, but I encountered an error: {str(e)}"
        
        assistant_message = ChatMessage.objects.create(
            session=chat_session,
            role='assistant',
            content=error_message
        )
        
        return Response({
            'session_id': session_id,
            'message': error_message,
            'error': True,
            'messages': [
                {
                    'role': user_message.role,
                    'content': user_message.content,
                    'created_at': user_message.created_at.isoformat()
                },
                {
                    'role': assistant_message.role,
                    'content': assistant_message.content,
                    'created_at': assistant_message.created_at.isoformat()
                }
            ]
        }, status=status.HTTP_200_OK)


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


@api_view(['POST'])
def chat_with_functions(request):
    """
    Intelligent chat with Amadeus function calling via OpenRouter.
    
    POST /api/chat/functions/
    
    Request body:
    {
        "session_id": "optional-existing-session-id",
        "message": "User's message in natural language"
    }
    
    Response includes:
    - session_id: Chat session ID
    - message: Assistant's response
    - function_calls: List of Amadeus functions that were called
    - messages: Recent conversation messages
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
        chat_session = ChatSession.objects.create(
            session_id=session_id,
            workflow_state={'conversation_history': []}
        )
    
    # Save user message
    user_message = ChatMessage.objects.create(
        session=chat_session,
        role='user',
        content=message_content
    )
    
    # Process with OpenRouter function calling service
    try:
        # Initialize function calling service
        function_service = OpenRouterFunctionCallingService()
        
        # Get conversation history from session
        conversation_history = chat_session.workflow_state.get('conversation_history', [])
        
        # Process the message with function calling
        result = function_service.chat_with_function_calling(
            user_message=message_content,
            conversation_history=conversation_history
        )
        
        # Update session with new conversation history
        chat_session.workflow_state = {'conversation_history': result['conversation']}
        chat_session.save()
        
        # Create assistant response message
        assistant_response = result['response']
        assistant_message = ChatMessage.objects.create(
            session=chat_session,
            role='assistant',
            content=assistant_response,
            metadata={
                'function_calls': result.get('function_calls', []),
                'success': result.get('success', True)
            }
        )
        
        # Return response
        return Response({
            'session_id': session_id,
            'message': assistant_response,
            'function_calls': result.get('function_calls', []),
            'success': result.get('success', True),
            'messages': [
                {
                    'role': user_message.role,
                    'content': user_message.content,
                    'created_at': user_message.created_at.isoformat()
                },
                {
                    'role': assistant_message.role,
                    'content': assistant_message.content,
                    'created_at': assistant_message.created_at.isoformat()
                }
            ]
        })
        
    except ValueError as e:
        # API key not configured
        error_message = str(e)
        if 'OpenRouter' in error_message:
            error_message = "Function calling service is not configured. Please set OPENROUTER_API_KEY environment variable."
        
        # Create fallback response
        assistant_message = ChatMessage.objects.create(
            session=chat_session,
            role='assistant',
            content=error_message
        )
        
        return Response({
            'session_id': session_id,
            'message': error_message,
            'error': True,
            'messages': [
                {
                    'role': user_message.role,
                    'content': user_message.content,
                    'created_at': user_message.created_at.isoformat()
                },
                {
                    'role': assistant_message.role,
                    'content': assistant_message.content,
                    'created_at': assistant_message.created_at.isoformat()
                }
            ]
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        # Unexpected error
        error_message = f"I apologize, but I encountered an error: {str(e)}"
        
        assistant_message = ChatMessage.objects.create(
            session=chat_session,
            role='assistant',
            content=error_message
        )
        
        return Response({
            'session_id': session_id,
            'message': error_message,
            'error': True,
            'messages': [
                {
                    'role': user_message.role,
                    'content': user_message.content,
                    'created_at': user_message.created_at.isoformat()
                },
                {
                    'role': assistant_message.role,
                    'content': assistant_message.content,
                    'created_at': assistant_message.created_at.isoformat()
                }
            ]
        }, status=status.HTTP_200_OK)


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
