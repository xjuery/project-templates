# Configuration Keycloak

Ce guide vous explique comment configurer Keycloak pour l'application Angular-FastAPI-OIDC.

## 1. Démarrer Keycloak avec Docker Compose

```bash
# Démarrer Keycloak
docker-compose up -d

# Vérifier que le conteneur est en cours d'exécution
docker-compose ps

# Voir les logs
docker-compose logs -f keycloak
```

Keycloak sera disponible à : http://localhost:8080

## 2. Accéder à la Console d'Administration Keycloak

1. Ouvrez : http://localhost:8080
2. Cliquez sur "Administration Console"
3. Connectez-vous avec :
   - Username: `admin`
   - Password: `admin`

## 3. Créer un Client pour l'Application Angular

### Option A: Utiliser le realm Master (Simple pour le développement)

1. Dans la console Keycloak, sélectionnez le realm **Master** (déjà par défaut)
2. Dans le menu de gauche, cliquez sur **Clients**
3. Cliquez sur **Create client**
4. Configurez le client :
   - **Client ID**: `angular-client`
   - **Client authentication**: OFF (Public client)
   - Cliquez sur **Next**

5. Configurez les paramètres :
   - **Root URL**: `http://localhost:4200`
   - **Valid redirect URIs**: `http://localhost:4200/*`
   - **Valid post logout redirect URIs**: `http://localhost:4200/*`
   - **Web origins**: `*`
   - ⚠️ **Important pour PKCE** : Dans l'onglet **Advanced Settings**, vérifiez que :
     - **Proof Key for Code Exchange (PKCE) Code Challenge Method** : `S256` ou `plain`
     - **PKCE Code Challenge Method** : Activé
   - Cliquez sur **Save**

### Option B: Créer un Nouveau Realm (Recommandé pour la production)

1. Créez un nouveau realm :
   - Cliquez sur le dropdown en haut à gauche
   - Cliquez sur **Create Realm**
   - Nom du realm: `myapp`
   - Cliquez sur **Create**

2. Créez un utilisateur de test :
   - Allez dans **Users** > **Add user**
   - **Username**: `alice`
   - **Email**: `alice@example.com`
   - Activez **Email Verified**
   - Cliquez sur **Create**
   - Allez dans l'onglet **Credentials**
   - Définissez un mot de passe
   - **Temporary**: OFF
   - Cliquez sur **Save**

3. Configurez le client comme dans l'Option A

## 4. Configurer l'Application

Si vous avez créé un nouveau realm, mettez à jour les configurations :

### Frontend (environment.ts)
```typescript
oidcIssuer: 'http://localhost:8080/auth/realms/myapp',  // Votre realm
```

### Backend (app/main.py)
```python
OIDC_ISSUER = "http://localhost:8080/auth/realms/myapp"  // Votre realm
```

## 5. Utilisateurs de Test

### Realm Master (par défaut)
Par défaut, le realm `master` a un utilisateur admin :
- Username: `admin`
- Password: `admin`

### Créer d'Autres Utilisateurs

1. Dans **Users** > **Add user**
2. Remplissez les informations
3. Allez dans **Credentials** > Définissez un mot de passe
4. **Temporary**: OFF
5. **Save**

### Importer des Utilisateurs en Masse

Keycloak permet l'import en masse d'utilisateurs via CSV ou via l'API.

Pour ajouter des utilisateurs via la console web :
1. **Users** > **Add user**
2. Remplir les champs obligatoires
3. Aller dans **Credentials** et définir un mot de passe
4. Répéter pour chaque utilisateur

## 6. Configuration OIDC

Keycloak expose automatiquement les endpoints OIDC :
- Configuration: `http://localhost:8080/auth/realms/{realm-name}/.well-known/openid-configuration`
- Authorization: `http://localhost:8080/auth/realms/{realm-name}/protocol/openid-connect/auth`
- Token: `http://localhost:8080/auth/realms/{realm-name}/protocol/openid-connect/token`
- JWKS: `http://localhost:8080/auth/realms/{realm-name}/protocol/openid-connect/certs`

## 7. Tester la Configuration

1. Démarrez Keycloak : `docker-compose up -d`
2. Démarrez le backend : `cd backend && ./run.sh`
3. Démarrez le frontend : `cd frontend && npm start`
4. Ouvrez http://localhost:4200
5. Cliquez sur "Login" et connectez-vous avec vos identifiants Keycloak

## 8. Commandes Utiles

```bash
# Arrêter Keycloak
docker-compose down

# Redémarrer Keycloak
docker-compose restart

# Voir les logs
docker-compose logs -f

# Accéder au shell du conteneur
docker-compose exec keycloak /bin/bash

# Supprimer complètement Keycloak (supprime les données)
docker-compose down -v
```

## 9. Export/Import de Configuration

Pour sauvegarder votre configuration Keycloak :

```bash
# Exporter le realm
docker-compose exec keycloak /opt/keycloak/bin/kc.sh export \
  --dir /opt/keycloak/data/import \
  --realm myapp

# Importer un realm
docker-compose exec keycloak /opt/keycloak/bin/kc.sh import \
  --dir /opt/keycloak/data/import
```

## 10. Problèmes Courants

### "Invalid redirect URI"
- Vérifiez que l'URI de redirection dans la configuration du client correspond à l'URL de votre application

### "Client not found"
- Vérifiez que le Client ID dans votre configuration correspond au Client ID dans Keycloak

### "Connection refused"
- Vérifiez que Keycloak est bien démarré : `docker-compose ps`
- Vérifiez les logs : `docker-compose logs keycloak`

### "Access Denied"
- Vérifiez que l'utilisateur a bien les droits d'accès au realm
- Vérifiez les roles de l'utilisateur

## 11. Configuration PKCE (Proof Key for Code Exchange)

Cette application utilise le flux **Authorization Code + PKCE**, qui est recommandé pour les clients publics (applications SPA).

### Configuration dans Keycloak

Pour activer PKCE dans Keycloak pour votre client :

1. Allez dans **Clients** > Sélectionnez votre client
2. Ouvrez l'onglet **Advanced settings**
3. Dans **Proof Key for Code Exchange (PKCE) Code Challenge Method** :
   - Sélectionnez `S256` (SHA-256) - Recommandé pour la production
   - Ou `plain` pour les tests de développement
4. Assurez-vous que **PKCE** est activé
5. **Save**

### Comment fonctionne PKCE

1. **Code Challenge** : Le client génère un code verifier aléatoire et le hash avec SHA-256
2. **Authorization Request** : Le code challenge est envoyé à Keycloak avec la requête d'autorisation
3. **Authorization Code** : Keycloak retourne un code d'autorisation
4. **Token Exchange** : Le client échange le code + le code verifier original contre le token
5. **Validation** : Keycloak vérifie que le code verifier correspond au code challenge

### Avantages de PKCE

- ✅ Protection contre les attaques par interception du code d'autorisation
- ✅ Recommandé par l'OAuth 2.0 Security Best Current Practice
- ✅ Particulièrement important pour les clients publics (SPA)
- ✅ Support natif par angular-oauth2-oidc

## 12. Sécurité en Production

Pour un déploiement en production :
1. Changez les mots de passe par défaut
2. Utilisez HTTPS
3. Créez un realm dédié (pas le realm master)
4. Configurez des rôles et des permissions appropriés
5. Activez l'authentification à deux facteurs si nécessaire
6. Configurez des policies de mots de passe strictes
7. Utilisez une base de données réelle (pas H2 en production)

