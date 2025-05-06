"""UI views for the chat application."""

from django.shortcuts import redirect
from django.views.generic import TemplateView

from app_chat.models import Conversation


class ChatUIListView(TemplateView):
    """Render the list of conversations."""

    template_name = "app_chat/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['conversations'] = Conversation.objects.all()
        return context

    def post(self, request):
        """Create a new conversation and redirect to its detail view."""

        conv = Conversation.objects.create()
        return redirect('chat-ui-detail', pk=conv.id)


class ChatUIConversationView(TemplateView):
    """Render a single conversation and its messages."""

    template_name = "app_chat/conversation.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['conversation_id'] = kwargs.get('pk')
        return context
