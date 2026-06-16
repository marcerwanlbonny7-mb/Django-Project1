from django.db import models
from django.conf import settings


class FormuleAssurance(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    prix_mensuel = models.DecimalField(max_digits=10, decimal_places=2)
    couverture = models.TextField()

    class Meta:
        ordering = ['prix_mensuel']

    def __str__(self):
        return self.nom


class Souscription(models.Model):
    class Statut(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active'
        EXPIREE = 'EXPIREE', 'Expirée'
        RESILIEE = 'RESILIEE', 'Résiliée'

    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='souscriptions',
        limit_choices_to={'role': 'CLIENT'},
    )
    formule = models.ForeignKey(FormuleAssurance, on_delete=models.CASCADE, related_name='souscriptions')
    date_debut = models.DateField()
    date_fin = models.DateField()
    statut = models.CharField(max_length=10, choices=Statut.choices, default=Statut.ACTIVE)
    notif_envoyee = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_debut']

    def __str__(self):
        return f"{self.client.username} - {self.formule.nom} - {self.get_statut_display()}"
