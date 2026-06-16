from rest_framework import generics, permissions
from .models import FormuleAssurance, Souscription
from .serializers import FormuleAssuranceSerializer, SouscriptionSerializer, ResilierSerializer
from users.permissions import EstClient


class FormuleAssuranceListView(generics.ListAPIView):
    queryset = FormuleAssurance.objects.all()
    serializer_class = FormuleAssuranceSerializer
    permission_classes = [permissions.AllowAny]


class SouscriptionCreateView(generics.CreateAPIView):
    queryset = Souscription.objects.all()
    serializer_class = SouscriptionSerializer
    permission_classes = [permissions.IsAuthenticated, EstClient]


class MesPolicesView(generics.ListAPIView):
    serializer_class = SouscriptionSerializer

    def get_queryset(self):
        return Souscription.objects.filter(client=self.request.user)


class ResilierSouscriptionView(generics.UpdateAPIView):
    queryset = Souscription.objects.all()
    serializer_class = ResilierSerializer
    permission_classes = [permissions.IsAuthenticated, EstClient]

    def perform_update(self, serializer):
        souscription = self.get_object()
        if souscription.client != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Vous ne pouvez résilier que vos propres souscriptions.")
        souscription.statut = Souscription.Statut.RESILIEE
        souscription.save()
