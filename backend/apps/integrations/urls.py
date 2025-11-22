from django.urls import path
from . import views

urlpatterns = [
    path('services/', views.services_list, name='services-list'),
    path('services/<int:service_id>/', views.service_detail, name='service-detail'),
    path('logs/', views.api_logs, name='api-logs'),
    path('health/', views.service_health, name='service-health'),
    path('activities/', views.get_activities, name='activities'),
]
