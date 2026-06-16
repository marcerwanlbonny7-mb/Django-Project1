from django.db import models
from django.conf import settings
from django.utils import timezone


class Conversation(models.Model):
    class Statut(models.TextChoices):
        OUVERTE = 'OUVERTE', 'Ouverte'
        EN_COURS = 'EN_COURS', 'En cours'
        FERMEE = 'FERMEE', 'Fermée'

    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='conversations_client',
        limit_choices_to={'role': 'CLIENT'},
    )
    agent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='conversations_agent',
        limit_choices_to={'role__in': ['AGENT', 'ADMIN']},
    )
    statut = models.CharField(max_length=10, choices=Statut.choices, default=Statut.OUVERTE)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Conversation {self.id} - {self.client.username} ({self.get_statut_display()})"


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    auteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    contenu = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    lu = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.auteur.username}: {self.contenu[:50]}"
