from rest_framework import serializers
from .models import Concessionnaire, Vehicule
import random


def _generate_siret():
    return ''.join(str(random.randint(0, 9)) for _ in range(14))


class ConcessionnaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Concessionnaire
        fields = ['id', 'nom']

    def create(self, validated_data):
        validated_data['siret'] = _generate_siret()
        return super().create(validated_data)


class VehiculeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicule
        fields = ['id', 'concessionnaire', 'type', 'marque', 'chevaux', 'prix_ht']
