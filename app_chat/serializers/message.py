"""Serializer for Message model."""

from rest_framework import serializers
from app_chat.models import Message


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for Message model."""

    class Meta:
        """Meta class for MessageSerializer."""

        model = Message
        fields = ("id", "direction", "content", "timestamp")
        read_only_fields = ("id",)
