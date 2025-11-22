from rest_framework import serializers
from .models import ChatSession, ChatMessage


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'role', 'content', 'metadata', 'created_at']
        read_only_fields = ['created_at']


class ChatSessionSerializer(serializers.ModelSerializer):
    messages = ChatMessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = ChatSession
        fields = ['id', 'session_id', 'messages', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class ChatRequestSerializer(serializers.Serializer):
    """
    Serializer for chat message requests.
    """
    session_id = serializers.CharField(required=False, allow_blank=True)
    message = serializers.CharField(required=True)
