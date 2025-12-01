# Frontend minimal

Ce dossier contient une interface statique minimale pour interagir visuellement avec l'API.

Utilisation:

1. Démarrez le serveur Django depuis la racine du projet:

```
python manage.py runserver
```

2. Ouvrez `frontend/index.html` dans votre navigateur (idéalement via l'URL `http://127.0.0.1:8000/frontend/index.html` si vous servez les fichiers statiques avec Django, ou ouvrez le fichier localement et laissez les appels API pointer sur `http://127.0.0.1:8000` si CORS/Origine n'est pas un problème).

Remarques:
- L'interface utilise uniquement les endpoints GET listés dans le sujet.
- Conçu pour démonstration et test rapide; pas de build tool nécessaire.
