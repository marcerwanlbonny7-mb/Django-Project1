from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'destinataire', 'type', 'message', 'lu', 'created_at']
        read_only_fields = ['destinataire', 'type', 'message', 'created_at']
