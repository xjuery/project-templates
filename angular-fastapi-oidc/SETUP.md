# Guide de Configuration Rapide

Ce guide vous aidera à configurer et exécuter l'application d'intégration OAuth2/OIDC.

## Étape 1 : Démarrer Keycloak

Keycloak est fourni dans un conteneur Docker pour simplifier le développement.

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

## Étape 2 : Configurer Keycloak

Avant de démarrer le backend et le frontend, vous devez configurer Keycloak :

1. Accédez à http://localhost:8080
2. Cliquez sur "Administration Console"
3. Connectez-vous avec admin/admin
4. Créez le client `angular-client` comme décrit dans [KEYCLOAK_SETUP.md](KEYCLOAK_SETUP.md)

Consultez le guide détaillé pour la configuration complète.

## Étape 3 : Démarrer le Backend

```bash
cd backend

# Créez un environnement virtuel (recommandé)
python3 -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate

# Installez les dépendances
pip install -r requirements.txt

# Lancez le backend
./run.sh

# Ou directement :
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Le backend sera disponible sur http://localhost:8000

## Étape 4 : Démarrer le Frontend

```bash
cd frontend

# Installez les dépendances
npm install

# Démarrez le serveur de développement
npm start
```

Le frontend sera disponible sur http://localhost:4200

## Étape 5 : Tester l'Application

1. Ouvrez votre navigateur sur http://localhost:4200
2. Cliquez sur le bouton "Login"
3. Connectez-vous avec vos identifiants Keycloak (admin/admin pour l'admin)
4. Après l'authentification, vous serez redirigé
5. Naviguez vers "Profile" pour voir le contenu protégé
6. Cliquez sur "Logout" pour terminer la session

## Dépannage

### Keycloak Ne Démarre Pas

Si Keycloak ne démarre pas :
1. Vérifiez que Docker est installé et fonctionne
2. Vérifiez que le port 8080 n'est pas utilisé
3. Consultez les logs : `docker-compose logs keycloak`

### Erreurs CORS

Si vous voyez des erreurs CORS :
1. Vérifiez que le backend fonctionne sur le port 8000
2. Vérifiez la configuration CORS dans `backend/app/main.py`
3. Assurez-vous que l'origine du frontend correspond aux origines autorisées

### Authentification Ne Fonctionne Pas

Si l'authentification échoue :
1. Vérifiez que Keycloak fonctionne sur le port 8080
2. Vérifiez la console du navigateur pour les erreurs
3. Assurez-vous que le Client ID correspond dans le frontend et Keycloak
4. Videz le cache et les cookies du navigateur

### Problèmes de Connexion au Backend

1. Vérifiez que le backend est en cours d'exécution
2. Vérifiez que Keycloak est accessible
3. Vérifiez les logs du backend pour les erreurs

## Prochaines Étapes

- Consultez [KEYCLOAK_SETUP.md](KEYCLOAK_SETUP.md) pour la configuration détaillée de Keycloak
- Consultez le README.md principal pour les détails de l'architecture
- Personnalisez la configuration dans `frontend/src/environments/environment.ts`
- Ajoutez plus d'endpoints protégés dans le backend
- Implémentez des rôles et des permissions utilisateur

