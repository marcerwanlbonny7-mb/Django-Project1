from django.db.models import Sum, Avg
from django.utils import timezone
from datetime import timedelta


def calculer_score(demande):
    score = 0
    client = demande.client

    from .models import DemandeCredit, Echeance

    credits_en_cours = DemandeCredit.objects.filter(
        client=client,
        statut__in=['SOUMISE', 'EN_ANALYSE', 'APPROUVEE', 'DECAISSEE']
    ).exclude(id=demande.id).count()

    if credits_en_cours == 0:
        score += 40

    from remboursements.models import Paiement
    echeances_client = Echeance.objects.filter(credit__client=client)
    total_echeances = echeances_client.count()
    if total_echeances > 0:
        total_du = echeances_client.aggregate(total=Sum('montant_du'))['total'] or 0
        total_paye = echeances_client.aggregate(total=Sum('montant_paye'))['total'] or 0
        if total_du > 0 and (total_paye / total_du) > 0.9:
            score += 30

    anciennete = timezone.now() - client.date_joined
    if anciennete > timedelta(days=180):
        score += 20

    if demande.montant < 500000:
        score += 10

    return min(score, 100)
