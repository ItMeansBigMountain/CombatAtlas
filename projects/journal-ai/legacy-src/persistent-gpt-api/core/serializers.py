from rest_framework import serializers
from .models import CustomUser, ChatSession, ChatMessage

# Custom User Serializer
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'profile_pic', 'oauth_provider', 'unique_identifier')
        # Include additional fields as per your CustomUser model

# Chat Session Serializer
class ChatSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatSession
        fields = ('session_id', 'user', 'session_data', 'created_at', 'updated_at', 'status')
        read_only_fields = ('created_at', 'updated_at')

# Chat Message Serializer
class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ('session', 'text', 'timestamp')