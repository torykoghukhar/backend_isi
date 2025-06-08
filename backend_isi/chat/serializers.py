from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Thread, Message


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class ThreadSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    participant_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True, write_only=True, source="participants"
    )

    class Meta:
        model = Thread
        fields = ['id', 'participants', 'participant_ids', 'created', 'updated']

    def validate_participants(self, participants):
        if len(participants) != 2:
            raise serializers.ValidationError("Thread must have exactly 2 participants.")
        return participants


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'text', 'thread', 'created', 'is_read']
        read_only_fields = ['sender', 'created', 'is_read']

    def validate_text(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message text cannot be empty.")
        return value
