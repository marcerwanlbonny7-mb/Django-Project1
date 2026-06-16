from django.db import models
from rest_framework import serializers
from .models import Paiement
from credits.models import Echeance


class PaiementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paiement
        fields = ['id', 'echeance', 'agent', 'montant', 'date_paiement', 'mode_paiement']
        read_only_fields = ['agent', 'date_paiement']

    def create(self, validated_data):
        validated_data['agent'] = self.context['request'].user
        paiement = super().create(validated_data)
        echeance = paiement.echeance
        total_paye = echeance.paiements.aggregate(
            total=models.Sum('montant')
        )['total'] or 0
        echeance.montant_paye = total_paye
        if total_paye >= echeance.montant_du:
            echeance.statut = Echeance.Statut.PAYEE
        echeance.save()
        return paiement


class EcheanceListSerializer(serializers.ModelSerializer):
    credit_id = serializers.IntegerField(source='credit.id')
    client_nom = serializers.CharField(source='credit.client.username')
    montant_restant = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    total_a_payer = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Echeance
        fields = [
            'id', 'credit_id', 'client_nom',
            'date_echeance', 'montant_du', 'montant_paye', 'montant_restant',
            'penalite', 'jours_retard', 'total_a_payer', 'statut',
        ]


class HistoriquePaiementSerializer(serializers.ModelSerializer):
    client_nom = serializers.CharField(source='echeance.credit.client.username', read_only=True)
    agent_nom = serializers.CharField(source='agent.username', read_only=True)

    class Meta:
        model = Paiement
        fields = ['id', 'echeance', 'client_nom', 'agent_nom', 'montant', 'date_paiement', 'mode_paiement']
