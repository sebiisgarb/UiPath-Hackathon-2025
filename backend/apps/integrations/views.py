from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import os
import asyncio
import httpx

from .models import ExternalService, APILog
from .serializers import ExternalServiceSerializer, APILogSerializer
from services.amadeus_client import AmadeusClient


@api_view(['GET', 'POST'])
def services_list(request):
    """
    List all external services or create a new one.
    
    GET /api/integrations/services/
    POST /api/integrations/services/
    """
    if request.method == 'GET':
        services = ExternalService.objects.all()
        serializer = ExternalServiceSerializer(services, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ExternalServiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def service_detail(request, service_id):
    """
    Get, update or delete an external service.
    
    GET /api/integrations/services/{service_id}/
    PUT /api/integrations/services/{service_id}/
    DELETE /api/integrations/services/{service_id}/
    """
    try:
        service = ExternalService.objects.get(id=service_id)
    except ExternalService.DoesNotExist:
        return Response(
            {'error': 'Service not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    if request.method == 'GET':
        serializer = ExternalServiceSerializer(service)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = ExternalServiceSerializer(service, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        service.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def api_logs(request):
    """
    List API logs with optional filtering.
    
    GET /api/integrations/logs/
    """
    logs = APILog.objects.all()
    
    # Filter by service if provided
    service_id = request.query_params.get('service_id')
    if service_id:
        logs = logs.filter(service_id=service_id)
    
    # Limit to recent logs
    limit = int(request.query_params.get('limit', 100))
    logs = logs[:limit]
    
    serializer = APILogSerializer(logs, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def service_health(request):
    """
    Check health status of all active services.
    
    GET /api/integrations/health/
    """
    services = ExternalService.objects.filter(is_active=True)
    
    health_status = []
    for service in services:
        # In production, this would actually ping the service
        health_status.append({
            'service': service.name,
            'type': service.service_type,
            'status': 'healthy',  # Mock status
            'endpoint': service.api_endpoint
        })
    
    return Response({
        'status': 'ok',
        'services': health_status
    })


@api_view(['GET'])
def get_activities(request):
    """
    Get activities from Amadeus API.
    
    GET /api/integrations/activities/
    
    Query parameters:
    - latitude: float (required)
    - longitude: float (required)
    - radius: int (optional, default: 3)
    - min_price: float (optional)
    - max_price: float (optional)
    - limit: int (optional)
    - sort_by_rating: bool (optional, default: false)
    """
    # Get query parameters
    try:
        latitude = float(request.query_params.get('latitude'))
        longitude = float(request.query_params.get('longitude'))
    except (TypeError, ValueError):
        return Response(
            {'error': 'latitude and longitude are required and must be valid numbers'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Parse radius with error handling
    try:
        radius = int(request.query_params.get('radius', 3))
    except (TypeError, ValueError):
        return Response(
            {'error': 'radius must be a valid integer'},
            status=status.HTTP_400_BAD_REQUEST
        )
    min_price = request.query_params.get('min_price')
    max_price = request.query_params.get('max_price')
    limit = request.query_params.get('limit')
    sort_by_rating = request.query_params.get('sort_by_rating', 'false').lower() == 'true'
    
    # Convert to proper types if provided
    if min_price:
        try:
            min_price = float(min_price)
        except ValueError:
            return Response(
                {'error': 'min_price must be a valid number'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    if max_price:
        try:
            max_price = float(max_price)
        except ValueError:
            return Response(
                {'error': 'max_price must be a valid number'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    if limit:
        try:
            limit = int(limit)
        except ValueError:
            return Response(
                {'error': 'limit must be a valid integer'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    # Get Amadeus credentials from environment
    client_id = os.environ.get('AMADEUS_CLIENT_ID')
    client_secret = os.environ.get('AMADEUS_CLIENT_SECRET')
    
    if not client_id or not client_secret:
        return Response(
            {'error': 'Amadeus API credentials not configured'},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )
    
    # Create Amadeus client and fetch activities
    try:
        amadeus_client = AmadeusClient(client_id, client_secret)
        
        # Run async function using asyncio.run for better compatibility
        activities = asyncio.run(
            amadeus_client.get_activities(
                latitude=latitude,
                longitude=longitude,
                radius=radius,
                min_price=min_price,
                max_price=max_price,
                limit=limit,
                sort_by_rating=sort_by_rating
            )
        )
        
        return Response(activities, status=status.HTTP_200_OK)
    
    except httpx.HTTPStatusError as e:
        return Response(
            {
                'error': 'Failed to fetch activities from Amadeus API',
                'detail': str(e)
            },
            status=status.HTTP_502_BAD_GATEWAY
        )
    except Exception as e:
        return Response(
            {
                'error': 'An error occurred while fetching activities',
                'detail': str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
