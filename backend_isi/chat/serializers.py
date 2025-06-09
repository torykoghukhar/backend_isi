from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Thread, Message


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class ThreadSerializer(serializers.ModelSerializer):
    receiver_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True
    )
    participants = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Thread
        fields = ['id', 'receiver_id', 'participants', 'created', 'updated']

    def create(self, validated_data):
        user1 = self.context['request'].user
        user2 = validated_data['receiver_id']

        if user1 == user2:
            raise serializers.ValidationError("You can't create a thread with yourself.")

        existing_threads = Thread.objects.filter(participants=user1).filter(participants=user2)
        for thread in existing_threads:
            if set(thread.participants.values_list("id", flat=True)) == {user1.id, user2.id}:
                return thread

        thread = Thread.objects.create()
        thread.participants.set([user1, user2])
        return thread


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
