from django.db import models
from django.conf import settings
from django.utils import timezone
from credits.models import Echeance


class Paiement(models.Model):
    class ModePaiement(models.TextChoices):
        ORANGE_MONEY = 'ORANGE_MONEY', 'Orange Money'
        WAVE = 'WAVE', 'Wave'
        MTN_MOMO = 'MTN_MOMO', 'MTN MoMo'
        ESPECES = 'ESPECES', 'Espèces'

    echeance = models.ForeignKey(Echeance, on_delete=models.CASCADE, related_name='paiements')
    agent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='paiements_enregistres',
    )
    montant = models.DecimalField(max_digits=12, decimal_places=2)
    date_paiement = models.DateTimeField(default=timezone.now)
    mode_paiement = models.CharField(max_length=15, choices=ModePaiement.choices)

    class Meta:
        ordering = ['-date_paiement']

    def __str__(self):
        return f"Paiement {self.id} - {self.montant} FCFA - {self.get_mode_paiement_display()}"
