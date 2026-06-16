from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer, AssignerSerializer
from users.permissions import EstClient, EstAdmin
from users.serializers import AgentPresenceSerializer

User = get_user_model()


class AgentListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        agents = User.objects.filter(role__in=['AGENT', 'ADMIN'])
        serializer = AgentPresenceSerializer(agents, many=True)
        return Response(serializer.data)


class ConversationListCreateView(generics.ListCreateAPIView):
    serializer_class = ConversationSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'CLIENT':
            return Conversation.objects.filter(client=user)
        return Conversation.objects.all()

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), EstClient()]
        return [permissions.IsAuthenticated()]


class MessageListView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        return Message.objects.filter(conversation_id=self.kwargs['pk']).select_related('auteur')

    def perform_create(self, serializer):
        serializer.save(auteur=self.request.user, conversation_id=self.kwargs['pk'])


class AssignerConversationView(generics.UpdateAPIView):
    queryset = Conversation.objects.all()
    serializer_class = AssignerSerializer
    permission_classes = [permissions.IsAuthenticated, EstAdmin]

    def perform_update(self, serializer):
        conversation = self.get_object()
        conversation.agent = self.request.user
        conversation.statut = Conversation.Statut.EN_COURS
        conversation.save()
