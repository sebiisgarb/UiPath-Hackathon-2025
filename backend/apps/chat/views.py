from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from services.chatbot_service import ChatbotService


# Initialize chatbot service
chatbot_service = ChatbotService()


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
    
    if session_id:
        chatbot_service.reset_session(session_id)
    
    return Response({'message': 'Session reset successful'})

