"""Model representing a message within a conversation."""

import uuid

from django.db import models

from app_chat.models import Conversation


class Message(models.Model):
    """Model representing a message within a conversation."""

    DIRECTION_SENT = "SENT"
    DIRECTION_RECEIVED = "RECEIVED"
    DIRECTION_CHOICES = [
        (DIRECTION_SENT, "Sent"),
        (DIRECTION_RECEIVED, "Received"),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages"
    )
    direction = models.CharField(
        max_length=8,
        choices=DIRECTION_CHOICES
    )
    content = models.TextField()
    timestamp = models.DateTimeField()
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.direction} at {self.timestamp}"
