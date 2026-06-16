from django.db import models
from django.conf import settings
from django.utils import timezone


class Notification(models.Model):
    class Type(models.TextChoices):
        CREDIT = 'CREDIT', 'Crédit'
        REMBOURSEMENT = 'REMBOURSEMENT', 'Remboursement'
        ASSURANCE = 'ASSURANCE', 'Assurance'
        CHAT = 'CHAT', 'Chat'

    destinataire = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
    )
    type = models.CharField(max_length=15, choices=Type.choices)
    message = models.TextField()
    lu = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.get_type_display()}] {self.destinataire.username} - {self.message[:50]}"
