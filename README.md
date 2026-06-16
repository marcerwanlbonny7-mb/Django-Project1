# COFINANCE CI — Plateforme Digitale

API REST Django + Frontend HTML/CSS/JS vanilla pour la digitalisation des opérations de microfinance et d'assurance mobile de COFINANCE CI (Abidjan, Côte d'Ivoire).

---

## Stack Technique

| Couche | Technologie |
|--------|-------------|
| Backend | Python 3.11+ / Django 5.x / DRF |
| Auth | JWT (djangorestframework-simplejwt) |
| WebSocket | Django Channels + Daphne |
| Documentation | drf-spectacular (Swagger / Redoc) |
| Base de données | SQLite (dev) / PostgreSQL (prod) |
| Frontend | HTML5 + CSS3 + JavaScript vanilla |

---

## Installation

### 1. Cloner le projet

```bash
git clone <votre-repo>
cd cofinance_ci
```

### 2. Créer l'environnement virtuel

```bash
python -m venv venv
```

Activer l'environnement :

- **Windows :**
  ```bash
  venv\Scripts\activate
  ```
- **Mac / Linux :**
  ```bash
  source venv/bin/activate
  ```

> Vous devriez voir `(venv)` apparaître dans votre terminal.

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configurer l'environnement

```bash
cp .env.example .env
```

Éditez `.env` si nécessaire (les valeurs par défaut fonctionnent pour le développement).

### 5. Appliquer les migrations

```bash
python manage.py migrate
```

### 6. Charger les données de démonstration

```bash
python manage.py seed_data
```

---

## Démarrage

```bash
python manage.py runserver
```

| Accès | URL |
|-------|-----|
| **Frontend** | http://localhost:8000/ |
| **API REST** | http://localhost:8000/api/ |
| **Swagger** | http://localhost:8000/api/docs/ |
| **Redoc** | http://localhost:8000/api/redoc/ |

> ⚠️ Si vous modifiez les fichiers du frontend, faites **Ctrl+F5** (hard refresh) dans le navigateur pour contourner le cache.

---

## Première connexion

| Rôle | Identifiant | Mot de passe |
|------|-------------|--------------|
| 🔑 Admin | `admin` | `admin123` |
| 🧑‍💼 Agent | `agent1` | `agent123` |
| 👤 Client | `inside` | `inside123` |

Connectez-vous depuis la page d'accueil → **Connexion**.

---

## Pages du Frontend

Toutes les pages sont servies par Django dans `/static/frontend/` :

| Page | URL | Accès |
|------|-----|-------|
| Accueil / Connexion | `/` | Public |
| Inscription | `/static/frontend/register.html` | Public |
| Dashboard client | `/static/frontend/dashboard_client.html` | Client |
| Dashboard admin | `/static/frontend/dashboard_admin.html` | Admin / Agent |
| Mes crédits | `/static/frontend/credits.html` | Client |
| Remboursements | `/static/frontend/remboursements.html` | Client |
| Assurances | `/static/frontend/assurances.html` | Client |
| Notifications | `/static/frontend/notifications.html` | Tous |
| Chat | `/static/frontend/chat.html` | Tous |

Fonctionnalités :
- JWT stocké dans `localStorage`, auto-refresh sur 401
- Sidebar responsive avec hamburger mobile
- Modales, toasts, spinners
- WebSocket chat temps réel avec indicateur de frappe et présence

---

## API REST — Endpoints

### Authentification (`/api/auth/`)
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/register/` | Inscription client |
| POST | `/login/` | Connexion (tokens JWT) |
| POST | `/token/refresh/` | Rafraîchir token |
| GET/PUT | `/profile/` | Consulter / modifier profil |

### Crédits (`/api/credits/`)
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/` | Soumettre une demande (client) |
| GET | `/` | Lister les demandes |
| GET | `/{id}/` | Détail d'une demande |
| PATCH | `/{id}/statut/` | Changer le statut (agent/admin) |
| GET | `/{id}/echeancier/` | Échéancier d'un crédit |

### Remboursements (`/api/remboursements/`)
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/` | Enregistrer un paiement (agent) |
| GET | `/echeances/` | Lister les échéances |
| GET | `/historique/` | Historique des paiements |

### Assurances (`/api/assurances/`)
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/formules/` | Catalogue des formules |
| POST | `/souscrire/` | Souscrire (client) |
| GET | `/mes-polices/` | Polices actives |
| PATCH | `/{id}/resilier/` | Résilier |

### Dashboard (`/api/dashboard/`)
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/stats/?date_debut=&date_fin=&agent=&region=` | Indicateurs (admin) |

### Notifications (`/api/notifications/`)
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/` | Lister les notifications |
| PATCH | `/{id}/lire/` | Marquer comme lue |
| PATCH | `/lire-tout/` | Tout marquer comme lu |

### Chat (`/api/chat/`)
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/agents/` | Liste des agents (présence incluse) |
| POST | `/conversations/` | Ouvrir une conversation (client) |
| GET | `/conversations/` | Lister les conversations |
| GET | `/conversations/{id}/messages/` | Messages d'une conversation |
| PATCH | `/conversations/{id}/assigner/` | Assigner un agent (admin) |

### WebSocket
| Protocole | URL | Description |
|-----------|-----|-------------|
| WS | `/ws/chat/{conversation_id}/` | Chat temps réel |

---

## Règles métier

- **Scoring d'éligibilité** — Calcul automatique à la soumission (max 100 pts, seuil 70 pts)
- **Intérêts** — `interets_totaux = montant * taux_interet / 100`
- **Pénalités de retard** — 2 % du montant restant dû, calculé à chaque sauvegarde d'échéance
- **Présence en ligne** — Détection temps réel via WebSocket
- **Indicateur de frappe** — Affiché quand un utilisateur tape un message
- **Alertes échéances** — Notification client à J-3 et J+1 ; notification agent à J+1
- **Expiration assurance** — Notification 15 jours avant la date de fin
- **Permissions par rôle** — CLIENT, AGENT, ADMIN avec accès distincts

---

## Structure du projet

```
cofinance_ci/
├── cofinance_ci/              # Configuration Django
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── users/                     # Authentification, profils, rôles
├── credits/                   # Microcrédits, scoring, intérêts
├── remboursements/            # Paiements, échéances
├── assurances/                # Catalogue, souscriptions
├── dashboard/                 # Indicateurs et statistiques
├── notifications/             # Alertes in-app
├── chat/                      # WebSocket, conversations, présence
├── static/frontend/           # Frontend HTML / CSS / JS
│   ├── css/style.css
│   ├── js/
│   │   ├── auth.js
│   │   ├── api.js
│   │   └── utils.js
│   ├── index.html
│   ├── register.html
│   ├── dashboard_client.html
│   ├── dashboard_admin.html
│   ├── credits.html
│   ├── remboursements.html
│   ├── assurances.html
│   ├── notifications.html
│   └── chat.html
├── templates/                 # Pages HTML legacy
├── fixtures/                  # Données de démonstration
└── media/                     # Uploads
```

---

## Commandes utiles

```bash
# Recréer la base de données
python manage.py flush
python manage.py seed_data

# Créer un super-utilisateur
python manage.py createsuperuser

# Lancer la console Django
python manage.py shell

# Collecter les fichiers statiques (production)
python manage.py collectstatic
```
