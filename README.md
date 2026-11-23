# LOG3550 — Devoir 2
## API de gestion d'un catalogue de bibliothèque

### 1. Description du projet

Ce projet consiste à développer une API REST permettant de gérer un catalogue de bibliothèque. L'application utilise FastAPI, SQLite et SQLModel pour le backend, ainsi que HTML, CSS et JavaScript pour le frontend.

L'API permet d'ajouter, consulter, rechercher, filtrer, modifier et supprimer des livres.

### 2. Technologies utilisées

- Python 3.14
- FastAPI
- Uvicorn
- SQLModel
- SQLite
- Pydantic
- Pytest
- HTTPX
- HTML5
- CSS3
- JavaScript
- Visual Studio Code
- Git et GitHub

### 3. Structure du projet

```text
LOG3550_D2/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── routers/
│       ├── __init__.py
│       └── livres.py
├── frontend/
│   ├── index.html
│   ├── css/
│   │   └── styles.css
│   └── js/
│       ├── app.js
│       └── data.js
├── tests/
│   └── test_livres.py
├── captures/
├── requirements.txt
├── README.md
└── .gitignore
```

### 4. Installation et configuration

Créer un environnement virtuel :

```powershell
python -m venv .venv
```

Activer l'environnement virtuel sous Windows PowerShell :

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Installer les dépendances :

```powershell
pip install -r requirements.txt
```

### 5. Lancement du backend

À la racine du projet, exécuter :

```powershell
uvicorn app.main:app --reload
```

L'API est accessible à :

http://127.0.0.1:8000

Documentation interactive Swagger :

http://127.0.0.1:8000/docs

Vérification de santé :

http://127.0.0.1:8000/sante

### 6. Fonctionnalités de l'API

| Méthode | Endpoint | Description |
|---|---|---|
| GET | /livres/ | Lister les livres |
| GET | /livres/{id} | Consulter un livre |
| POST | /livres/ | Ajouter un livre |
| PUT | /livres/{id} | Remplacer un livre |
| PATCH | /livres/{id} | Modifier certains champs |
| DELETE | /livres/{id} | Supprimer un livre |
| GET | /sante | Vérifier l'état de l'API |

La recherche peut être effectuée par titre ou auteur avec le paramètre `q`. Il est également possible de filtrer par catégorie et disponibilité.

La pagination est prise en charge avec les paramètres skip et limit. La valeur de skip doit être positive ou nulle et limit est compris entre 1 et 100.

### 7. Validation et gestion des erreurs

Les données sont validées avec Pydantic.

- Le titre et l'auteur doivent contenir entre 2 et 200 caractères.
- L'année doit être comprise entre 1450 et l'année actuelle.
- La catégorie doit être valide.
- L'ISBN doit contenir 10 ou 13 chiffres lorsqu'il est fourni.
- Un ISBN déjà utilisé entraîne une erreur 409.
- Un livre inexistant entraîne une erreur 404.
- Des données invalides entraînent une erreur 422.

### 8. Choix techniques

**FastAPI :** framework utilisé pour créer les endpoints de l'API REST.

**Uvicorn :** serveur ASGI utilisé pour exécuter l'application FastAPI.

**Pydantic :** bibliothèque utilisée pour valider les données reçues et retournées par l'API.

**Modèles et schémas :** les modèles SQLModel représentent les tables de la base de données, tandis que les schémas définissent les données acceptées et retournées par l'API.

**PUT et PATCH :** PUT remplace les données d'une ressource, tandis que PATCH modifie uniquement les champs transmis.

**Idempotence :** une opération idempotente produit le même état final lorsqu'elle est exécutée plusieurs fois avec les mêmes données. PUT et DELETE sont conçus comme des opérations idempotentes.

# ExPlication : Difference entre PUT et PATCH

PUT remplace complètement une ressource existante par les nouvelles données transmises.  
PATCH modifie uniquement les champs spécifiés sans remplacer toute la ressource.  
PUT est idempotent, car répéter la même requête produit le même état final de la ressource.  
DELETE est idempotent, car supprimer plusieurs fois la même ressource laisse toujours cette ressource absente.  
POST n'est pas idempotent, car répéter une requête peut créer plusieurs ressources différentes.

### 9. Base de données

La base de données utilisée est SQLite avec SQLModel.

Les tables sont créées automatiquement au démarrage de l'application. Huit livres de départ sont ajoutés lorsque la base de données est vide.

Les sessions de base de données sont gérées avec `Depends` et fermées après chaque requête.

### 10. Frontend

Le frontend utilise HTML, CSS et JavaScript sans framework.

Il communique avec le backend à l'aide de `fetch`, `async` et `await`.

Les fonctionnalités comprennent :

- Affichage des livres provenant de l'API.
- Recherche et filtrage.
- Tri des résultats.
- Ajout de livres.
- Suppression de livres.
- Affichage des messages de chargement et d'erreur.

Le frontend est lancé avec l'extension Live Server de Visual Studio Code à partir de `frontend/index.html`.

Le middleware CORS autorise les origines locales utilisées par Live Server.

### 11. Tests

Les tests automatisés sont réalisés avec Pytest et TestClient.

Pour exécuter les tests :

```powershell
python -m pytest -v
```

Les huit tests vérifient :

- La création d'un livre.
- La lecture des livres.
- Le filtrage.
- La modification.
- La suppression.
- La gestion d'un livre introuvable (404).
- La validation des données (422).
- La détection d'un ISBN dupliqué (409).

Résultat obtenu : **8 tests réussis**.

### 12. Difficultés rencontrées

- Configuration de l'environnement virtuel Python.
- Organisation des dossiers du projet.
- Configuration de la connexion entre le frontend et le backend.
- Gestion des erreurs de validation.
- Configuration du CORS.
- Mise en place des tests automatisés.

### 13. Outils et ressources utilisés

- Visual Studio Code
- Documentation officielle FastAPI
- Documentation Python
- Documentation SQLModel
- Pytest
- ChatGPT (assistance pour l'explication, le débogage et la vérification du projet).

### 14. Dépôt GitHub

Lien du dépôt GitHub :

https://github.com/BIGELY/LOG3550_D2