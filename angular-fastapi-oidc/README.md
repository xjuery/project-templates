# Angular-FastAPI-OIDC Integration

Une application à deux niveaux démontrant l'intégration OAuth2/OIDC entre un frontend Angular et un backend FastAPI, utilisant **Keycloak** pour l'authentification.

## Architecture

### Frontend (Angular)
- Utilise la librairie `angular-oauth2-oidc` pour l'authentification OAuth2/OIDC
- Implémente **Authorization Code Flow + PKCE** pour une sécurité renforcée
- Implémente des auth guards pour la protection des routes
- HTTP interceptor pour ajouter automatiquement les tokens Bearer aux requêtes API
- Composants protégés nécessitant l'authentification

### Backend (FastAPI)
- API REST avec validation JWT OAuth2/OIDC
- Endpoints pour le profil utilisateur et informations publiques
- Validation des tokens contre Keycloak
- CORS configuré pour l'accès au frontend

## Prérequis

- Node.js 18+ et npm
- Python 3.9+
- Docker et Docker Compose (pour Keycloak)

## Installation et Configuration

### 1. Démarrer Keycloak

Keycloak est fourni dans un conteneur Docker pour simplifier le développement :

```bash
# Démarrer Keycloak
docker-compose up -d

# Vérifier que le conteneur fonctionne
docker-compose ps
```

Keycloak sera disponible sur http://localhost:8080

**Identifiants Admin:**
- Username: `admin`
- Password: `admin`

Consultez [KEYCLOAK_SETUP.md](KEYCLOAK_SETUP.md) pour la configuration détaillée de Keycloak, y compris la création du client et des utilisateurs.

### 2. Configuration du Frontend

```bash
# Navigez vers le répertoire frontend
cd frontend

# Installez les dépendances
npm install

# Démarrez le serveur de développement
npm start

# Le frontend sera disponible sur http://localhost:4200
```

### 3. Configuration du Backend

```bash
# Navigez vers le répertoire backend
cd backend

# Créez un environnement virtuel (optionnel mais recommandé)
python3 -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate

# Installez les dépendances
pip install -r requirements.txt

# Lancez le backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Ou utilisez le script fourni
./run.sh

# Le backend sera disponible sur http://localhost:8000
```

## Utilisation

1. **Démarrez Keycloak**
   ```bash
   docker-compose up -d
   ```

2. **Configurez Keycloak** (voir [KEYCLOAK_SETUP.md](KEYCLOAK_SETUP.md))
   - Accédez à http://localhost:8080
   - Connectez-vous avec admin/admin
   - Créez le client `angular-client` comme décrit dans le guide

3. **Démarrez le backend FastAPI**
   ```bash
   cd backend
   pip install -r requirements.txt
   ./run.sh
   ```

4. **Démarrez le frontend Angular**
   ```bash
   cd frontend
   npm install
   npm start
   ```

5. **Ouvrez l'application**
   - Accédez à http://localhost:4200
   - Cliquez sur "Login" pour vous authentifier
   - Connectez-vous avec vos identifiants Keycloak
   - Naviguez vers "Profile" pour voir le contenu protégé

## API Endpoints

### Public Endpoints
- `GET /` - API root
- `GET /api/public/info` - Public information endpoint

### Protected Endpoints
- `GET /api/user/profile` - User profile (requires authentication)

## Configuration

### Frontend Configuration

Éditez `frontend/src/environments/environment.ts` pour changer :
- **OIDC Issuer URL** : URL du realm Keycloak (par défaut: `http://localhost:8080/auth/realms/master`)
- **Client ID** : ID du client configuré dans Keycloak (par défaut: `angular-client`)
- **Redirect URI** : URI de redirection (par défaut: `http://localhost:4200`)
- **API URL** : URL du backend (par défaut: `http://localhost:8000`)

### Backend Configuration

Éditez `backend/app/main.py` pour changer :
- **OIDC Issuer** : URL du realm Keycloak
- **CORS origins** : Origines autorisées
- **Token validation logic** : Logique de validation des tokens

## Détails de l'Architecture

### Flux d'Authentification (Code Flow + PKCE)

1. L'utilisateur clique sur "Login" dans le frontend
2. Le frontend génère un **code verifier** et un **code challenge** (PKCE)
3. Le frontend redirige vers Keycloak avec le code challenge
4. L'utilisateur s'authentifie avec Keycloak
5. Keycloak redirige avec le code d'autorisation
6. Le frontend échange le code + code verifier contre un access token
7. Keycloak valide que le code verifier correspond au code challenge (PKCE)
8. Le frontend stocke le token et l'inclut dans les requêtes API
9. Le backend valide le token avec Keycloak
10. Le backend retourne les données protégées

### Sécurité

- **Authorization Code Flow + PKCE** : Protection renforcée contre les attaques par interception
- L'intercepteur HTTP ajoute automatiquement l'en-tête `Authorization: Bearer <token>`
- L'auth guard protège les routes nécessitant l'authentification
- Le backend valide les tokens JWT de Keycloak
- CORS configuré pour n'autoriser que l'origine du frontend
- PKCE utilise SHA-256 (S256) pour le code challenge

## Notes de Développement

- Le backend a un fallback pour le décodage JWT en développement
- Le frontend est configuré avec `skipIssuerCheck: true` et `requireHttps: false` pour le développement
- Toutes les vérifications HTTPS sont désactivées pour le développement local

## Considérations pour la Production

Pour un déploiement en production :
1. Activez HTTPS et la validation des certificats
2. Configurez les origines CORS appropriées
3. Utilisez des variables d'environnement pour la configuration
4. Implémentez une logique de rafraîchissement des tokens
5. Ajoutez la gestion d'erreurs et la journalisation
6. Activez la vérification de signature JWT
7. Supprimez les bypasses de développement

## Dépannage

**Erreurs CORS:**
- Assurez-vous que le backend autorise l'origine du frontend
- Vérifiez que les serveurs fonctionnent sur les ports attendus

**Problèmes d'Authentification:**
- Vérifiez que Keycloak est en cours d'exécution
- Vérifiez la console pour les erreurs de token
- Assurez-vous que le Client ID correspond à la configuration Keycloak

**Erreurs de Connexion au Backend:**
- Vérifiez que le backend fonctionne sur le port 8000
- Vérifiez que l'URL de l'API dans le frontend pointe vers le bon backend
- Assurez-vous que CORS est correctement configuré

## Ressources

- [Documentation de Configuration Keycloak](KEYCLOAK_SETUP.md)
- [Guide de Démarrage Rapide](SETUP.md)
- [Configuration PKCE et Sécurité](PKCE_EXPLAINED.md)
- [Documentation Keycloak](https://www.keycloak.org/documentation)
- [Documentation angular-oauth2-oidc](https://github.com/manfredsteyer/angular-oauth2-oidc)
- [Documentation FastAPI](https://fastapi.tiangolo.com/)

## Licence

Ceci est une application d'exemple à des fins de démonstration.

