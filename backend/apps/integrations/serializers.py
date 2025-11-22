from rest_framework import serializers
from .models import ExternalService, APILog


class ExternalServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExternalService
        fields = [
            'id', 'name', 'service_type', 'api_endpoint', 
            'is_active', 'configuration', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
        # Don't expose API keys
        extra_kwargs = {
            'api_key': {'write_only': True}
        }


class APILogSerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(source='service.name', read_only=True)
    
    class Meta:
        model = APILog
        fields = [
            'id', 'service', 'service_name', 'endpoint', 'method',
            'request_data', 'response_status', 'response_data',
            'response_time_ms', 'error_message', 'created_at'
        ]
        read_only_fields = ['created_at']
