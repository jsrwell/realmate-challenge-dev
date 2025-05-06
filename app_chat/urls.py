"""URL configuration for the app_chat application."""

from django.urls import path

from app_chat.views import (ChatUIConversationView, ChatUIListView,
                            ConversationDetailView, WebhookView)

urlpatterns = [
    path("webhook/",
         WebhookView.as_view(),
         name="webhook"),
    path("conversations/<uuid:pk>/",
         ConversationDetailView.as_view(),
         name="conversation-detail"),
    path('ui/conversations/',
         ChatUIListView.as_view(),
         name='chat-ui-list'),
    path('ui/conversations/<uuid:pk>/',
         ChatUIConversationView.as_view(),
         name='chat-ui-detail'),
]
