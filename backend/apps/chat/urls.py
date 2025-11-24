from django.urls import path
from . import views
from .views import LocateCityView

urlpatterns = [
    path('', views.chat, name='chat'),
    path('reset/', views.reset, name='reset'),
    path('update_state/', views.update_state, name='update_state'),
    path('summary/', views.summary, name='summary'),
    path('locate_city/', LocateCityView.as_view(), name='locate_city'),
]
