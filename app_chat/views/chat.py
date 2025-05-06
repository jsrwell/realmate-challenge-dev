"""Handle webhook events and retrieve conversation details."""

import logging

from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from app_chat.models import Conversation, Message
from app_chat.serializers import ConversationSerializer

logger = logging.getLogger(__name__)


class WebhookView(APIView):
    """Handle incoming webhook events."""

    def post(self, request):
        """Process webhook POST and create/update models."""

        event_type = request.data.get("type")
        timestamp = request.data.get("timestamp")
        data = request.data.get("data", {})

        try:
            if event_type == "NEW_CONVERSATION":
                Conversation.objects.get_or_create(id=data["id"])

            elif event_type == "NEW_MESSAGE":
                conv = get_object_or_404(
                    Conversation, id=data["conversation_id"]
                )

                if conv.state == Conversation.STATE_CLOSED:
                    return Response(
                        {"error": "Conversation is closed"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                Message.objects.create(
                    id=data["id"],
                    conversation=conv,
                    direction=data["direction"],
                    content=data["content"],
                    timestamp=timestamp,
                )

            elif event_type == "CLOSE_CONVERSATION":
                conv = get_object_or_404(Conversation, id=data["id"])
                conv.state = Conversation.STATE_CLOSED
                conv.closed_at = timestamp
                conv.save()

            else:
                return Response(
                    {"error": "Invalid event type"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            return Response({"status": "success"}, status=status.HTTP_200_OK)

        except IntegrityError as e:
            logger.error("Integrity error: %s", e)
            return Response(
                {"error": "Integrity error"},
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            logger.error("Unexpected error: %s", e)
            return Response(
                {"error": "Unexpected error"},
                status=status.HTTP_400_BAD_REQUEST
            )


class ConversationDetailView(RetrieveAPIView):
    """Retrieve a conversation with its messages."""

    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
