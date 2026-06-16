from celery import shared_task
from django.utils import timezone
from datetime import timedelta, date
from credits.models import Echeance
from assurances.models import Souscription
from .models import Notification
from django.contrib.auth import get_user_model

User = get_user_model()


@shared_task
def verifier_echeances():
    aujourd_hui = timezone.now().date()
    resultats = []

    echeances_j3 = Echeance.objects.filter(
        date_echeance=aujourd_hui + timedelta(days=3),
        statut__in=['EN_ATTENTE', 'EN_RETARD'],
    )
    for echeance in echeances_j3:
        Notification.objects.create(
            destinataire=echeance.credit.client,
            type='REMBOURSEMENT',
            message=f"Rappel : votre échéance de {echeance.montant_du} FCFA arrive dans 3 jours (le {echeance.date_echeance}).",
        )
        resultats.append(f"Notification J-3 envoyée à {echeance.credit.client.username}")

    echeances_j1 = Echeance.objects.filter(
        date_echeance=aujourd_hui - timedelta(days=1),
        statut__in=['EN_ATTENTE'],
    )
    for echeance in echeances_j1:
        echeance.statut = Echeance.Statut.EN_RETARD
        echeance.save()

        Notification.objects.create(
            destinataire=echeance.credit.client,
            type='REMBOURSEMENT',
            message=f"ALERTE : votre échéance du {echeance.date_echeance} ({echeance.montant_du} FCFA) est en retard. Régularisez au plus vite.",
        )
        resultats.append(f"Notification retard envoyée à {echeance.credit.client.username}")

        for agent in User.objects.filter(role__in=['AGENT', 'ADMIN']):
            Notification.objects.create(
                destinataire=agent,
                type='REMBOURSEMENT',
                message=f"Client {echeance.credit.client.username} - Échéance {echeance.id} en retard ({echeance.montant_du} FCFA).",
            )

    return resultats


@shared_task
def verifier_assurances_expirant():
    aujourd_hui = timezone.now().date()
    resultats = []

    souscriptions_15j = Souscription.objects.filter(
        date_fin__lte=aujourd_hui + timedelta(days=15),
        date_fin__gte=aujourd_hui,
        statut='ACTIVE',
        notif_envoyee=False,
    )
    for souscription in souscriptions_15j:
        Notification.objects.create(
            destinataire=souscription.client,
            type='ASSURANCE',
            message=f"Votre assurance {souscription.formule.nom} expire le {souscription.date_fin}. Pensez à la renouveler.",
        )
        souscription.notif_envoyee = True
        souscription.save()
        resultats.append(f"Notification expiration envoyée à {souscription.client.username}")

    souscriptions_expirees = Souscription.objects.filter(
        date_fin__lt=aujourd_hui,
        statut='ACTIVE',
    )
    for souscription in souscriptions_expirees:
        souscription.statut = Souscription.Statut.EXPIREE
        souscription.save()
        resultats.append(f"Souscription {souscription.id} marquée comme expirée")

    return resultats
