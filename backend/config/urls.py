"""
URL configuration for AI Trip Planner backend project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/trips/', include('apps.trips.urls')),
    path('api/chat/', include('apps.chat.urls')),
    path('api/integrations/', include('apps.integrations.urls')),
]
