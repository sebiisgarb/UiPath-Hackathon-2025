from django.urls import path
from . import views

urlpatterns = [
    path('plan/', views.plan_trip, name='plan-trip'),
    path('', views.list_trips, name='list-trips'),
    path('<int:trip_id>/', views.get_trip_detail, name='trip-detail'),
]
