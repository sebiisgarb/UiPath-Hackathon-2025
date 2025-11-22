from django.db import models


class ExternalService(models.Model):
    """
    Represents external service integrations (flights APIs, hotel APIs, etc.)
    """
    SERVICE_TYPES = [
        ('flight', 'Flight API'),
        ('hotel', 'Hotel API'),
        ('activity', 'Activity API'),
        ('weather', 'Weather API'),
        ('translation', 'Translation API'),
        ('llm', 'LLM API'),
    ]
    
    name = models.CharField(max_length=100)
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPES)
    api_key = models.CharField(max_length=255, blank=True)
    api_endpoint = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    configuration = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.get_service_type_display()})"


class APILog(models.Model):
    """
    Logs API calls to external services for monitoring and debugging.
    """
    service = models.ForeignKey(
        ExternalService,
        on_delete=models.CASCADE,
        related_name='api_logs'
    )
    endpoint = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    request_data = models.JSONField(default=dict, blank=True)
    response_status = models.IntegerField(null=True, blank=True)
    response_data = models.JSONField(default=dict, blank=True)
    response_time_ms = models.IntegerField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.service.name} - {self.method} {self.endpoint} - {self.response_status}"
