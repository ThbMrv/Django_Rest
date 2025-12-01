# Projet: API Concessionnaire (Django REST)

Ce dépôt contient une API Django REST minimale pour gérer des concessionnaires et leurs véhicules.

Résumé rapide
- Modèles: `Concessionnaire(nom, siret)` et `Vehicule(type, marque, chevaux, prix_ht)`.
- L'API n'expose pas le champ `siret` (présent en base seulement).
- Endpoints GET requis implémentés. POST pour création de ressources disponibles pour tests.

Prérequis
- Python 3.10+ (ou votre installation Python 3.x)
- Windows: l'exemple ci‑dessous utilise `cmd.exe` (PowerShell fonctionne aussi).

Installation (rapide)
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Initialisation de la base et démarrage
```
python manage.py migrate
python manage.py createsuperuser   # optionnel, pour accéder à l'admin
python manage.py runserver
```

Accéder à l'application
- Frontend (démo) : http://127.0.0.1:8000/frontend/
- Admin Django : http://127.0.0.1:8000/admin/ (utilisez le superuser créé)

API (endpoints principaux)
- GET `/api/concessionnaires/` — liste des concessionnaires
- GET `/api/concessionnaires/<id>/` — détail d'un concessionnaire
- GET `/api/concessionnaires/<id>/vehicules/` — véhicules d'un concessionnaire
- GET `/api/concessionnaires/<id>/vehicules/<id>/` — détail d'un véhicule

Notes sur `siret`
- Le champ `siret` est stocké en base et validé (exactement 14 chiffres).
- Par contrainte du sujet, `siret` n'est **pas** exposé par l'API (ni en lecture, ni en écriture).
- Le backend génère automatiquement un `siret` lors de la création via l'API ; vous pouvez néanmoins le consulter/éditer depuis l'admin.

Documentation OpenAPI
- Swagger UI: http://127.0.0.1:8000/doc/  (installez les dépendances avec `pip install -r requirements.txt`)
- Schéma brut: http://127.0.0.1:8000/schema/

Tests rapides (exemples curl)
```
curl http://127.0.0.1:8000/api/concessionnaires/
curl http://127.0.0.1:8000/api/concessionnaires/1/
```

Conseils pour la remise
- Faites plusieurs commits clairs (ex: init, models+migration, api views, frontend, docs).
- Poussez le dépôt public GitHub et fournissez le lien dans votre rendu.

Besoin d'aide
- Je peux: préparer des commits propres, ajouter des fixtures de démonstration, ou implémenter le bonus JWT si nécessaire. Dites‑moi ce que vous voulez.
