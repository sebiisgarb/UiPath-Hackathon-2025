from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import ExternalService, APILog
from .serializers import ExternalServiceSerializer, APILogSerializer


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
