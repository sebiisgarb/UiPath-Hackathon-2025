from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from services.chatbot_service import ChatbotService
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse
from services.image_city_service import ImageCityService


def get_chatbot_service():
    """Lazy initialization of chatbot service."""
    if not hasattr(get_chatbot_service, '_instance'):
        get_chatbot_service._instance = ChatbotService()
    return get_chatbot_service._instance


@api_view(['GET', 'POST'])
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
    chatbot_service = get_chatbot_service()

    if request.method == 'GET':
        session_id = request.query_params.get('sessionId') or request.query_params.get('session_id') or request.headers.get('X-Session-Id')
        if not session_id:
            return Response({'error': 'sessionId query param required'}, status=status.HTTP_400_BAD_REQUEST)
        data = chatbot_service.get_session_data(session_id)
        if not data:
            return Response({'error': 'Session not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(data)

    # POST
    message = request.data.get('message')
    session_id = (
        request.data.get('sessionId')
        or request.data.get('session_id')
        or request.headers.get('X-Session-Id')
    )
    if not message:
        return Response({'error': 'Message is required'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        result = chatbot_service.process_message(message, session_id)
        return Response(result)
    except Exception as e:
        return Response({'error': 'Failed to process message', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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


@api_view(['POST'])
def update_state(request):
    """Partial update of workflow state (flight/hotel/activities/itinerary/progress_stage)."""
    chatbot_service = get_chatbot_service()
    session_id = (
        request.data.get('sessionId')
        or request.data.get('session_id')
        or request.headers.get('X-Session-Id')
    )
    if not session_id:
        return Response({'error': 'sessionId required'}, status=status.HTTP_400_BAD_REQUEST)
    updates = request.data.get('updates') or {}
    if not isinstance(updates, dict):
        return Response({'error': 'updates must be an object'}, status=status.HTTP_400_BAD_REQUEST)
    state = chatbot_service.update_state(session_id, updates)
    if state is None:
        return Response({'error': 'Session not found'}, status=status.HTTP_404_NOT_FOUND)
    return Response({'session_id': session_id, 'state': state})


@api_view(['GET'])
def summary(request):
    """Return a compact summary of current planning selections."""
    chatbot_service = get_chatbot_service()
    session_id = request.query_params.get('sessionId') or request.query_params.get('session_id') or request.headers.get('X-Session-Id')
    if not session_id:
        return Response({'error': 'sessionId required'}, status=status.HTTP_400_BAD_REQUEST)
    data = chatbot_service.get_session_data(session_id)
    if not data:
        return Response({'error': 'Session not found'}, status=status.HTTP_404_NOT_FOUND)
    state = data['state']
    summary_payload = {
        'session_id': session_id,
        'progress_stage': state.get('progress_stage'),
        'origin_airport': state.get('origin_airport'),
        'destination_airport': state.get('destination_airport'),
        'departure_date': state.get('departure_date'),
        'return_date': state.get('return_date'),
        'adults': state.get('adults'),
        'children': state.get('children'),
        'flight_selected': bool(state.get('flight_selection')),
        'hotel_selected': bool(state.get('hotel_selection')),
        'activities_count': len(state.get('activities_selection') or []),
        'itinerary_defined': bool(state.get('itinerary'))
    }
    return Response({'summary': summary_payload, 'state': state})


@method_decorator(csrf_exempt, name="dispatch")
class LocateCityView(View):
    def post(self, request):
        if not request.FILES.get("image"):
            return JsonResponse({"error": "Lipsește fișierul imagine"}, status=400)
        image_file = request.FILES["image"]
        user_hint = request.POST.get("hint")
        try:
            service = ImageCityService()
            analysis = service.analyze(image_file.read(), user_hint=user_hint)
            return JsonResponse({"data": analysis})
        except Exception as e:
            return JsonResponse({"error": f"Eroare internă: {str(e)}"}, status=500)

