from decimal import Decimal
from django.db import models
from django.conf import settings
from django.utils import timezone


class DemandeCredit(models.Model):
    class Statut(models.TextChoices):
        SOUMISE = 'SOUMISE', 'Soumise'
        EN_ANALYSE = 'EN_ANALYSE', 'En analyse'
        APPROUVEE = 'APPROUVEE', 'Approuvée'
        DECAISSEE = 'DECAISSEE', 'Décaissée'
        REJETEE = 'REJETEE', 'Rejetée'

    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='demandes_credit',
        limit_choices_to={'role': 'CLIENT'},
    )
    agent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='dossiers_traités',
        limit_choices_to={'role__in': ['AGENT', 'ADMIN']},
    )
    montant = models.DecimalField(max_digits=12, decimal_places=2)
    duree_mois = models.IntegerField()
    taux_interet = models.DecimalField(max_digits=5, decimal_places=2, default=5.00)
    motif = models.TextField()
    statut = models.CharField(max_length=15, choices=Statut.choices, default=Statut.SOUMISE)
    score_eligibilite = models.IntegerField(editable=False, default=0)
    interets_totaux = models.DecimalField(max_digits=12, decimal_places=2, editable=False, default=0)
    date_soumission = models.DateTimeField(default=timezone.now)
    date_decision = models.DateTimeField(null=True, blank=True)
    pieces_justificatives = models.FileField(upload_to='justificatifs/', blank=True, null=True)

    class Meta:
        ordering = ['-date_soumission']

    def save(self, *args, **kwargs):
        taux = Decimal(str(self.taux_interet)) if not isinstance(self.taux_interet, Decimal) else self.taux_interet
        self.interets_totaux = self.montant * taux / Decimal('100')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Demande {self.id} - {self.client.username} - {self.montant} FCFA"


class Echeance(models.Model):
    class Statut(models.TextChoices):
        EN_ATTENTE = 'EN_ATTENTE', 'En attente'
        PAYEE = 'PAYEE', 'Payée'
        EN_RETARD = 'EN_RETARD', 'En retard'

    credit = models.ForeignKey(DemandeCredit, on_delete=models.CASCADE, related_name='echeances')
    date_echeance = models.DateField()
    montant_du = models.DecimalField(max_digits=12, decimal_places=2)
    montant_paye = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    penalite = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    jours_retard = models.IntegerField(default=0)
    statut = models.CharField(max_length=15, choices=Statut.choices, default=Statut.EN_ATTENTE)

    class Meta:
        ordering = ['date_echeance']

    @property
    def montant_restant(self):
        return self.montant_du - self.montant_paye

    @property
    def total_a_payer(self):
        return self.montant_restant + self.penalite

    def calculer_penalite(self):
        if self.statut == self.Statut.PAYEE:
            self.penalite = 0
            self.jours_retard = 0
            return

        from django.utils import timezone
        today = timezone.now().date()
        if self.date_echeance < today:
            self.jours_retard = (today - self.date_echeance).days
            self.penalite = self.montant_restant * Decimal('0.02')
            if self.statut != self.Statut.EN_RETARD:
                self.statut = self.Statut.EN_RETARD
        else:
            self.jours_retard = 0
            self.penalite = 0

    def save(self, *args, **kwargs):
        self.calculer_penalite()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Échéance {self.id} - Crédit {self.credit.id} - {self.date_echeance}"
