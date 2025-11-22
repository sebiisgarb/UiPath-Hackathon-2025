from django.db import models
from django.contrib.auth.models import User


class TripRequest(models.Model):
    """
    Main trip request model that stores user's trip planning requests.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    user_message = models.TextField(help_text="Original user message/query")
    destination = models.CharField(max_length=200, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    travelers_count = models.IntegerField(default=1)
    preferences = models.JSONField(default=dict, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Trip to {self.destination} - {self.status}"


class FlightOption(models.Model):
    """
    Flight options generated for a trip request.
    """
    trip_request = models.ForeignKey(
        TripRequest, 
        on_delete=models.CASCADE, 
        related_name='flight_options'
    )
    
    airline = models.CharField(max_length=100)
    flight_number = models.CharField(max_length=20)
    departure_airport = models.CharField(max_length=100)
    arrival_airport = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    duration_minutes = models.IntegerField()
    stops = models.IntegerField(default=0)
    
    is_selected = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['price']
    
    def __str__(self):
        return f"{self.airline} {self.flight_number} - ${self.price}"


class HotelOption(models.Model):
    """
    Hotel options generated for a trip request.
    """
    trip_request = models.ForeignKey(
        TripRequest, 
        on_delete=models.CASCADE, 
        related_name='hotel_options'
    )
    
    hotel_name = models.CharField(max_length=200)
    address = models.TextField()
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    amenities = models.JSONField(default=list)
    room_type = models.CharField(max_length=100)
    
    is_selected = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['price_per_night']
    
    def __str__(self):
        return f"{self.hotel_name} - ${self.price_per_night}/night"


class ItineraryDay(models.Model):
    """
    Daily itinerary for a trip request.
    """
    trip_request = models.ForeignKey(
        TripRequest, 
        on_delete=models.CASCADE, 
        related_name='itinerary_days'
    )
    
    day_number = models.IntegerField()
    date = models.DateField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    activities = models.JSONField(default=list)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['day_number']
        unique_together = ['trip_request', 'day_number']
    
    def __str__(self):
        return f"Day {self.day_number}: {self.title}"
