from django.urls import path
from . import views

urlpatterns = [
    path('message/', views.send_message, name='send-message'),
    path('functions/', views.chat_with_functions, name='chat-with-functions'),
    path('session/<str:session_id>/', views.get_session, name='get-session'),
    path('sessions/', views.list_sessions, name='list-sessions'),
]
