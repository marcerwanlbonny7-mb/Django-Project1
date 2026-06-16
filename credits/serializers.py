from rest_framework import serializers
from .models import DemandeCredit, Echeance


class DemandeCreditSerializer(serializers.ModelSerializer):
    client_nom = serializers.CharField(source='client.username', read_only=True)
    agent_nom = serializers.CharField(source='agent.username', read_only=True, default=None)

    class Meta:
        model = DemandeCredit
        fields = [
            'id', 'client', 'client_nom', 'agent', 'agent_nom',
            'montant', 'duree_mois', 'taux_interet', 'motif', 'statut',
            'score_eligibilite', 'interets_totaux',
            'date_soumission', 'date_decision',
            'pieces_justificatives',
        ]
        read_only_fields = ['client', 'statut', 'score_eligibilite', 'interets_totaux', 'date_soumission', 'date_decision']

    def create(self, validated_data):
        from .scoring import calculer_score
        validated_data['client'] = self.context['request'].user
        demande = DemandeCredit(**validated_data)
        demande.score_eligibilite = calculer_score(demande)
        if demande.score_eligibilite >= 70:
            demande.statut = DemandeCredit.Statut.APPROUVEE
        demande.save()
        return demande


class StatutUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemandeCredit
        fields = ['statut']


class EcheanceSerializer(serializers.ModelSerializer):
    montant_restant = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    total_a_payer = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Echeance
        fields = [
            'id', 'credit', 'date_echeance',
            'montant_du', 'montant_paye', 'montant_restant',
            'penalite', 'jours_retard', 'total_a_payer', 'statut',
        ]
