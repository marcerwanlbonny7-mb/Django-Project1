from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Paiement
from credits.models import Echeance
from .serializers import PaiementSerializer, EcheanceListSerializer, HistoriquePaiementSerializer
from users.permissions import EstAgentOuAdmin


class PaiementCreateView(generics.CreateAPIView):
    queryset = Paiement.objects.all()
    serializer_class = PaiementSerializer
    permission_classes = [permissions.IsAuthenticated, EstAgentOuAdmin]


class EcheanceListView(generics.ListAPIView):
    serializer_class = EcheanceListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['statut']

    def get_queryset(self):
        user = self.request.user
        if user.role == 'CLIENT':
            return Echeance.objects.filter(credit__client=user)
        return Echeance.objects.all()


class HistoriquePaiementView(generics.ListAPIView):
    serializer_class = HistoriquePaiementSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['mode_paiement', 'echeance__credit__client']
    ordering = ['-date_paiement']

    def get_queryset(self):
        user = self.request.user
        if user.role == 'CLIENT':
            return Paiement.objects.filter(echeance__credit__client=user)
        return Paiement.objects.all()
