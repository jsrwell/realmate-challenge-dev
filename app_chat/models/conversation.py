"""Models for conversation state management."""

import uuid

from django.db import models


class Conversation(models.Model):
    """Model representing a conversation state."""

    STATE_OPEN = "OPEN"
    STATE_CLOSED = "CLOSED"
    STATE_CHOICES = [
        (STATE_OPEN, "Em Andamento"),
        (STATE_CLOSED, "Fechado"),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    state = models.CharField(
        max_length=6,
        choices=STATE_CHOICES,
        default=STATE_OPEN
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    closed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Conversation {self.id} ({self.state})"
