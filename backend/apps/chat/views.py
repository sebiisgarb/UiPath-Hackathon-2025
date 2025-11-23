from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from services.chatbot_service import ChatbotService


def get_chatbot_service():
    """Lazy initialization of chatbot service."""
    if not hasattr(get_chatbot_service, '_instance'):
        get_chatbot_service._instance = ChatbotService()
    return get_chatbot_service._instance


@api_view(['POST'])
def chat(request):
    """
    Handle chat messages with tool-calling orchestration.
    
    POST /chat
    
    Request body:
    {
        "message": "User's message",
        "sessionId": "optional-existing-session-id"
    }
    
    Response:
    {
        "reply": "final LLM message",
        "state": {...},
        "history": [...],
        "session_id": "session-id"
    }
    """
    message = request.data.get('message')
    session_id = request.data.get('sessionId')
    
    if not message:
        return Response(
            {'error': 'Message is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        chatbot_service = get_chatbot_service()
        result = chatbot_service.process_message(message, session_id)
        return Response(result)
    except Exception as e:
        return Response(
            {
                'error': 'Failed to process message',
                'details': str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def reset(request):
    """
    Reset a chat session.
    
    POST /reset
    
    Request body:
    {
        "sessionId": "session-id"
    }
    
    Response:
    {
        "message": "Session reset successful"
    }
    """
    session_id = request.data.get('sessionId')
    
    try:
        chatbot_service = get_chatbot_service()
        if session_id:
            chatbot_service.reset_session(session_id)
        
        return Response({'message': 'Session reset successful'})
    except Exception as e:
        return Response(
            {
                'error': 'Failed to reset session',
                'details': str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

