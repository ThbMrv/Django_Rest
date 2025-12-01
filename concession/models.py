from django.db import models
from django.core.validators import RegexValidator


class Concessionnaire(models.Model):
    nom = models.CharField(max_length=64)
    # siret must be exactly 14 digits; store in DB but do not expose via the API
    siret = models.CharField(
        max_length=14,
        validators=[RegexValidator(regex=r'^\d{14}$', message='Le SIRET doit contenir exactement 14 chiffres.')],
        help_text='SIRET (14 chiffres), généré automatiquement pour les créations API',
    )

    def __str__(self):
        return f"{self.nom}"


class Vehicule(models.Model):
    TYPE_CHOICES = [
        ('moto', 'Moto'),
        ('auto', 'Auto'),
    ]

    concessionnaire = models.ForeignKey(Concessionnaire, related_name='vehicules', on_delete=models.CASCADE)
    type = models.CharField(max_length=4, choices=TYPE_CHOICES)
    marque = models.CharField(max_length=64)
    chevaux = models.IntegerField()
    prix_ht = models.FloatField()

    def __str__(self):
        return f"{self.marque} ({self.type})"
