from django.contrib import admin
from .models import ExternalService, APILog


class APILogInline(admin.TabularInline):
    model = APILog
    extra = 0
    readonly_fields = ['created_at']
    fields = ['endpoint', 'method', 'response_status', 'response_time_ms', 'created_at']


@admin.register(ExternalService)
class ExternalServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'service_type', 'is_active', 'created_at']
    list_filter = ['service_type', 'is_active']
    search_fields = ['name', 'api_endpoint']
    inlines = [APILogInline]


@admin.register(APILog)
class APILogAdmin(admin.ModelAdmin):
    list_display = ['service', 'method', 'endpoint', 'response_status', 'response_time_ms', 'created_at']
    list_filter = ['service', 'method', 'response_status', 'created_at']
    search_fields = ['endpoint', 'error_message']
    readonly_fields = ['created_at']
