from rest_framework import serializers
from .models import Conversation, Message


class MessageSerializer(serializers.ModelSerializer):
    auteur_nom = serializers.CharField(source='auteur.username', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'conversation', 'auteur', 'auteur_nom', 'contenu', 'timestamp', 'lu']
        read_only_fields = ['auteur', 'timestamp', 'lu']


class ConversationSerializer(serializers.ModelSerializer):
    client_nom = serializers.CharField(source='client.username', read_only=True)
    agent_nom = serializers.CharField(source='agent.username', read_only=True, default=None)
    dernier_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            'id', 'client', 'client_nom', 'agent', 'agent_nom',
            'statut', 'created_at', 'dernier_message',
        ]
        read_only_fields = ['client', 'statut', 'created_at']

    def get_dernier_message(self, obj):
        msg = obj.messages.last()
        if msg:
            return {
                'contenu': msg.contenu[:100],
                'auteur_nom': msg.auteur.username,
                'timestamp': msg.timestamp,
            }
        return None

    def create(self, validated_data):
        validated_data['client'] = self.context['request'].user
        return super().create(validated_data)


class AssignerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = []
