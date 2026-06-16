from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.permissions import EstAdmin
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import timedelta
from credits.models import DemandeCredit, Echeance
from assurances.models import Souscription
from chat.models import Conversation


class DashboardStatsView(APIView):
    permission_classes = [IsAuthenticated, EstAdmin]

    def get(self, request):
        date_debut = request.query_params.get('date_debut')
        date_fin = request.query_params.get('date_fin')
        agent_id = request.query_params.get('agent')
        region = request.query_params.get('region')

        credits_qs = DemandeCredit.objects.all()
        echeances_qs = Echeance.objects.all()
        souscriptions_qs = Souscription.objects.all()
        conversations_qs = Conversation.objects.all()

        if date_debut:
            credits_qs = credits_qs.filter(date_soumission__gte=date_debut)
        if date_fin:
            credits_qs = credits_qs.filter(date_soumission__lte=date_fin)
        if agent_id:
            credits_qs = credits_qs.filter(agent_id=agent_id)
        if region:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            clients_region = User.objects.filter(region=region, role='CLIENT')
            credits_qs = credits_qs.filter(client__in=clients_region)

        demandes_par_statut = credits_qs.values('statut').annotate(
            count=Count('id')
        ).order_by('statut')

        total_du = echeances_qs.aggregate(total=Sum('montant_du'))['total'] or 0
        total_paye = echeances_qs.aggregate(total=Sum('montant_paye'))['total'] or 0
        taux_recouvrement = round((total_paye / total_du * 100), 2) if total_du > 0 else 0

        souscriptions_actives = souscriptions_qs.filter(statut='ACTIVE').count()
        conversations_ouvertes = conversations_qs.filter(
            statut__in=['OUVERTE', 'EN_COURS']
        ).count()

        return Response({
            'demandes_par_statut': list(demandes_par_statut),
            'total_demandes': credits_qs.count(),
            'total_du': total_du,
            'total_paye': total_paye,
            'taux_recouvrement': taux_recouvrement,
            'souscriptions_actives': souscriptions_actives,
            'conversations_ouvertes': conversations_ouvertes,
        })
