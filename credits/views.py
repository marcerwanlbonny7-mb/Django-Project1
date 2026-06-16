from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import DemandeCredit, Echeance
from .serializers import DemandeCreditSerializer, StatutUpdateSerializer, EcheanceSerializer
from users.permissions import EstClient, EstAgentOuAdmin, EstProprietaireOuAgentOuAdmin


class DemandeCreditListCreateView(generics.ListCreateAPIView):
    serializer_class = DemandeCreditSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['statut']
    search_fields = ['client__username', 'motif']
    ordering_fields = ['date_soumission', 'montant']

    def get_queryset(self):
        user = self.request.user
        if user.role == 'CLIENT':
            return DemandeCredit.objects.filter(client=user)
        return DemandeCredit.objects.all()

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), EstClient()]
        return [permissions.IsAuthenticated(), EstProprietaireOuAgentOuAdmin()]


class DemandeCreditDetailView(generics.RetrieveAPIView):
    queryset = DemandeCredit.objects.all()
    serializer_class = DemandeCreditSerializer
    permission_classes = [permissions.IsAuthenticated, EstProprietaireOuAgentOuAdmin]


class DemandeCreditStatutUpdateView(generics.UpdateAPIView):
    queryset = DemandeCredit.objects.all()
    serializer_class = StatutUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, EstAgentOuAdmin]

    def perform_update(self, serializer):
        from django.utils import timezone
        serializer.save(date_decision=timezone.now())


class EcheancierView(generics.ListAPIView):
    serializer_class = EcheanceSerializer

    def get_queryset(self):
        return Echeance.objects.filter(credit_id=self.kwargs['pk'])
