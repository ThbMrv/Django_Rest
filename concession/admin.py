from django.contrib import admin
from .models import Concessionnaire, Vehicule


@admin.register(Concessionnaire)
class ConcessionnaireAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'siret')


@admin.register(Vehicule)
class VehiculeAdmin(admin.ModelAdmin):
    list_display = ('id', 'marque', 'type', 'chevaux', 'prix_ht', 'concessionnaire')
