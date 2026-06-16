from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from users.models import UserProfile
from credits.models import DemandeCredit, Echeance
from remboursements.models import Paiement
from assurances.models import FormuleAssurance, Souscription
from notifications.models import Notification
from chat.models import Conversation, Message
from datetime import datetime, date, timedelta, timezone

User = get_user_model()


class Command(BaseCommand):
    help = 'Charge les données de démonstration pour COFINANCE CI'

    def handle(self, *args, **options):
        self.stdout.write('Création des utilisateurs...')

        admin = User.objects.create_superuser(
            username='admin', email='admin@cofinance.ci',
            password='admin123', role='ADMIN',
            phone='+2250101020304', region='Abidjan',
        )
        UserProfile.objects.create(user=admin, adresse='Abidjan Plateau')

        agent1 = User.objects.create_user(
            username='agent1', email='agent1@cofinance.ci',
            password='agent123', role='AGENT',
            phone='+2250102030405', region='Abidjan',
            first_name='Kouamé', last_name='Konan',
        )
        UserProfile.objects.create(user=agent1, adresse='Abidjan Cocody')

        agent2 = User.objects.create_user(
            username='agent2', email='agent2@cofinance.ci',
            password='agent123', role='AGENT',
            phone='+2250304050607', region='Yamoussoukro',
            first_name='Aminata', last_name='Diallo',
        )
        UserProfile.objects.create(user=agent2, adresse='Yamoussoukro Centre')

        client1 = User.objects.create_user(
            username='client1', email='client1@email.ci',
            password='client123', role='CLIENT',
            phone='+2250506070809', region='Abidjan',
            first_name='Marcel', last_name='Zadi',
            date_joined=datetime(2024, 6, 1, tzinfo=timezone.utc),
        )
        UserProfile.objects.create(user=client1, adresse='Abidjan Treichville')

        client2 = User.objects.create_user(
            username='client2', email='client2@email.ci',
            password='client123', role='CLIENT',
            phone='+2250708091011', region='Bouaké',
            first_name='Fatou', last_name='Sow',
            date_joined=datetime(2024, 9, 15, tzinfo=timezone.utc),
        )
        UserProfile.objects.create(user=client2, adresse='Bouaké Liberté')

        client3 = User.objects.create_user(
            username='client3', email='client3@email.ci',
            password='client123', role='CLIENT',
            phone='+2250910111213', region='Abidjan',
            first_name='Koffi', last_name='N\'Guessan',
            date_joined=datetime(2025, 3, 1, tzinfo=timezone.utc),
        )
        UserProfile.objects.create(user=client3, adresse='Abidjan Yopougon')

        self.stdout.write('Création des demandes de crédit...')

        d1 = DemandeCredit.objects.create(
            client=client1, agent=agent1,
            montant=250000, duree_mois=6,
            motif='Achat de matériel pour mon commerce',
            statut='DECAISSEE', score_eligibilite=100,
            date_soumission=datetime(2025, 3, 10, 8, 0, tzinfo=timezone.utc),
            date_decision=datetime(2025, 3, 12, 10, 0, tzinfo=timezone.utc),
        )

        d2 = DemandeCredit.objects.create(
            client=client2, agent=agent1,
            montant=500000, duree_mois=12,
            motif='Financement de ma boutique',
            statut='APPROUVEE', score_eligibilite=90,
            date_soumission=datetime(2025, 4, 5, 9, 0, tzinfo=timezone.utc),
            date_decision=datetime(2025, 4, 7, 14, 0, tzinfo=timezone.utc),
        )

        d3 = DemandeCredit.objects.create(
            client=client1, agent=None,
            montant=150000, duree_mois=3,
            motif='Réparation véhicule',
            statut='SOUMISE', score_eligibilite=100,
            date_soumission=datetime(2025, 6, 10, 11, 0, tzinfo=timezone.utc),
        )

        d4 = DemandeCredit.objects.create(
            client=client3, agent=None,
            montant=800000, duree_mois=12,
            motif='Construction maison',
            statut='SOUMISE', score_eligibilite=60,
            date_soumission=datetime(2025, 6, 12, 15, 0, tzinfo=timezone.utc),
        )

        d5 = DemandeCredit.objects.create(
            client=client2, agent=agent2,
            montant=200000, duree_mois=6,
            motif='Achat de bétail',
            statut='REJETEE', score_eligibilite=40,
            date_soumission=datetime(2025, 5, 20, 7, 0, tzinfo=timezone.utc),
            date_decision=datetime(2025, 5, 22, 16, 0, tzinfo=timezone.utc),
        )

        self.stdout.write('Création des échéances et paiements...')

        for i in range(6):
            Echeance.objects.create(
                credit=d1,
                date_echeance=date(2025, 4 + i, 10),
                montant_du=44166.67,
                montant_paye=44166.67 if i < 3 else (20000 if i == 3 else 0),
                statut='PAYEE' if i < 3 else 'EN_ATTENTE',
            )

        for i in range(4):
            Echeance.objects.create(
                credit=d2,
                date_echeance=date(2025, 5 + i, 5),
                montant_du=45833.33,
                montant_paye=45833.33 if i < 2 else 0,
                statut='PAYEE' if i < 2 else 'EN_ATTENTE',
            )

        Paiement.objects.create(
            echeance=Echeance.objects.get(credit=d1, date_echeance=date(2025, 4, 10)),
            agent=agent1, montant=44166.67,
            date_paiement=datetime(2025, 4, 10, 12, 0, tzinfo=timezone.utc),
            mode_paiement='ORANGE_MONEY',
        )
        Paiement.objects.create(
            echeance=Echeance.objects.get(credit=d1, date_echeance=date(2025, 5, 10)),
            agent=agent1, montant=44166.67,
            date_paiement=datetime(2025, 5, 10, 14, 0, tzinfo=timezone.utc),
            mode_paiement='WAVE',
        )
        Paiement.objects.create(
            echeance=Echeance.objects.get(credit=d1, date_echeance=date(2025, 6, 10)),
            agent=agent1, montant=44166.67,
            date_paiement=datetime(2025, 6, 10, 10, 0, tzinfo=timezone.utc),
            mode_paiement='MTN_MOMO',
        )
        Paiement.objects.create(
            echeance=Echeance.objects.get(credit=d1, date_echeance=date(2025, 7, 10)),
            agent=agent1, montant=20000,
            date_paiement=datetime(2025, 6, 28, 9, 0, tzinfo=timezone.utc),
            mode_paiement='ESPECES',
        )
        Paiement.objects.create(
            echeance=Echeance.objects.get(credit=d2, date_echeance=date(2025, 5, 5)),
            agent=agent1, montant=45833.33,
            date_paiement=datetime(2025, 5, 5, 11, 0, tzinfo=timezone.utc),
            mode_paiement='ORANGE_MONEY',
        )
        Paiement.objects.create(
            echeance=Echeance.objects.get(credit=d2, date_echeance=date(2025, 6, 5)),
            agent=agent1, montant=45833.33,
            date_paiement=datetime(2025, 6, 5, 15, 0, tzinfo=timezone.utc),
            mode_paiement='WAVE',
        )

        self.stdout.write('Création des formules d\'assurance...')

        f1 = FormuleAssurance.objects.create(
            nom='Assurance Vie',
            description='Protection décès et invalidité permanente',
            prix_mensuel=5000,
            couverture='Décès : 5 000 000 FCFA\nInvalidité permanente : 3 000 000 FCFA\nFrais funéraires : 500 000 FCFA',
        )
        f2 = FormuleAssurance.objects.create(
            nom='Assurance Santé',
            description='Couverture médicale pour toute la famille',
            prix_mensuel=15000,
            couverture='Consultations : 100%\nHospitalisation : 80%\nMédicaments : 70%',
        )
        f3 = FormuleAssurance.objects.create(
            nom='Assurance Crédit',
            description='Protection en cas d\'impayé lié à un accident',
            prix_mensuel=3000,
            couverture='Prise en charge des échéances en cas de perte d\'emploi\nRemboursement du capital décès',
        )

        Souscription.objects.create(
            client=client1, formule=f1,
            date_debut=date(2025, 1, 1), date_fin=date(2025, 12, 31),
            statut='ACTIVE',
        )
        Souscription.objects.create(
            client=client1, formule=f3,
            date_debut=date(2025, 3, 10), date_fin=date(2026, 3, 10),
            statut='ACTIVE',
        )
        Souscription.objects.create(
            client=client2, formule=f2,
            date_debut=date(2024, 6, 1), date_fin=date(2025, 6, 1),
            statut='EXPIREE', notif_envoyee=True,
        )
        Souscription.objects.create(
            client=client3, formule=f1,
            date_debut=date(2025, 4, 1), date_fin=date(2025, 10, 1),
            statut='ACTIVE',
        )

        self.stdout.write('Création des conversations...')

        conv1 = Conversation.objects.create(
            client=client1, agent=agent1, statut='EN_COURS',
            created_at=datetime(2025, 6, 1, 9, 0, tzinfo=timezone.utc),
        )
        conv2 = Conversation.objects.create(
            client=client2, agent=None, statut='OUVERTE',
            created_at=datetime(2025, 6, 13, 14, 0, tzinfo=timezone.utc),
        )

        Message.objects.create(
            conversation=conv1, auteur=client1,
            contenu='Bonjour, j\'aimerais avoir des informations sur mon crédit en cours.',
            timestamp=datetime(2025, 6, 1, 9, 1, tzinfo=timezone.utc), lu=True,
        )
        Message.objects.create(
            conversation=conv1, auteur=agent1,
            contenu='Bonjour Marcel ! Bien sûr, votre crédit de 250 000 FCFA est bien remboursé à 70%. Que voulez-vous savoir ?',
            timestamp=datetime(2025, 6, 1, 9, 5, tzinfo=timezone.utc), lu=True,
        )
        Message.objects.create(
            conversation=conv1, auteur=client1,
            contenu='Je voudrais savoir si je peux augmenter le montant de mon prochain crédit.',
            timestamp=datetime(2025, 6, 1, 9, 10, tzinfo=timezone.utc), lu=False,
        )
        Message.objects.create(
            conversation=conv2, auteur=client2,
            contenu='Bonjour, je souhaite souscrire à une assurance santé.',
            timestamp=datetime(2025, 6, 13, 14, 5, tzinfo=timezone.utc), lu=False,
        )

        self.stdout.write('Création des notifications...')

        Notification.objects.create(
            destinataire=client1, type='REMBOURSEMENT',
            message='Rappel : votre échéance du 10 juillet 2025 (44 166,67 FCFA) approche.',
        )
        Notification.objects.create(
            destinataire=client1, type='CREDIT',
            message='Votre demande de crédit n°3 a été soumise avec succès.',
            created_at=datetime(2025, 6, 10, 11, 0, tzinfo=timezone.utc),
        )
        Notification.objects.create(
            destinataire=client3, type='CREDIT',
            message='Votre demande de crédit n°4 a été soumise avec succès. Score : 60/100.',
            created_at=datetime(2025, 6, 12, 15, 0, tzinfo=timezone.utc),
        )

        Notification.objects.update_or_create(
            destinataire=client1, type='ASSURANCE',
            defaults={
                'message': 'Votre souscription à l\'Assurance Vie est active.',
                'lu': True,
            }
        )

        self.stdout.write(self.style.SUCCESS('Données de démonstration créées avec succès !'))
        self.stdout.write(self.style.SUCCESS('Admin  : admin / admin123'))
        self.stdout.write(self.style.SUCCESS('Agents : agent1 / agent123, agent2 / agent123'))
        self.stdout.write(self.style.SUCCESS('Clients: client1 / client123, client2 / client123, client3 / client123'))
