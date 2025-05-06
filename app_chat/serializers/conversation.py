"""Serializers for Conversation model."""

from rest_framework import serializers
from app_chat.models import Conversation
from app_chat.serializers import MessageSerializer


class ConversationSerializer(serializers.ModelSerializer):
    """Serializer for Conversation model with nested messages."""

    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        """Meta class for ConversationSerializer."""

        model = Conversation
        fields = ("id", "state", "messages")
