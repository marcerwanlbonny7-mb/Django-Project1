from rest_framework import serializers
from .models import FormuleAssurance, Souscription


class FormuleAssuranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormuleAssurance
        fields = ['id', 'nom', 'description', 'prix_mensuel', 'couverture']


class SouscriptionSerializer(serializers.ModelSerializer):
    formule_nom = serializers.CharField(source='formule.nom', read_only=True)

    class Meta:
        model = Souscription
        fields = ['id', 'client', 'formule', 'formule_nom', 'date_debut', 'date_fin', 'statut']
        read_only_fields = ['client', 'statut']

    def create(self, validated_data):
        validated_data['client'] = self.context['request'].user
        return super().create(validated_data)


class ResilierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Souscription
        fields = []
