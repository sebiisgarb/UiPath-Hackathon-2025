from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat, name='chat'),
    path('reset/', views.reset, name='reset'),
]
