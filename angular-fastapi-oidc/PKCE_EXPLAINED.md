# PKCE (Proof Key for Code Exchange) - Explication

## Qu'est-ce que PKCE ?

PKCE est une extension de sécurité pour le flux Authorization Code Flow d'OAuth 2.0. Il a été conçu pour protéger les clients publics (comme les applications Single Page Application - SPA) contre les attaques par interception du code d'autorisation.

## Problème que PKCE résout

Dans le flux Authorization Code standard, le code d'autorisation est transmis via l'URL de redirection. Un attaquant pourrait potentiellement :

1. Intercepter le code d'autorisation lors de la redirection
2. Utiliser ce code pour obtenir des tokens d'accès
3. Accéder aux ressources protégées

## Solution PKCE

PKCE introduit une preuve de possession (proof of possession) qui garantit que seule l'application qui a initié la demande d'autorisation peut échanger le code contre des tokens.

## Fonctionnement Technique

### 1. Génération (côté client)

```typescript
// 1. Générer un code verifier aléatoire (base64url)
codeVerifier = generateRandomBase64URLString(32) // ~128 bits
// Exemple: dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk

// 2. Générer le code challenge (hash SHA-256 du code verifier)
codeChallenge = base64url(sha256(codeVerifier))
// Exemple: E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM
```

### 2. Requête d'Authorization

Le client envoie le code challenge à l'autorisation serveur :

```
GET /auth/authorize?
  client_id=angular-client
  &response_type=code
  &code_challenge=E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM
  &code_challenge_method=S256
  &redirect_uri=http://localhost:4200
```

### 3. Obtention du code

Le serveur d'autorisation retourne un code d'autorisation qui est lié au code challenge :

```
Location: http://localhost:4200/callback?
  code=abc123xyz
```

### 4. Échange du code

Le client échange le code + code verifier contre le token :

```
POST /auth/token
  grant_type=authorization_code
  &code=abc123xyz
  &code_verifier=dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk
  &redirect_uri=http://localhost:4200
```

### 5. Validation

Le serveur :
1. Hash le code verifier avec SHA-256
2. Compare le résultat avec le code challenge stocké
3. Si correspond, émet le token

## Types de Code Challenge

### S256 (SHA-256) - Recommandé ✅

```typescript
codeChallenge = base64url(sha256(codeVerifier))
```

**Avantages :**
- Plus sécurisé (one-way hash)
- Ne révèle pas le code verifier
- Recommandé par la RFC 7636

### Plain - Pour tests uniquement

```typescript
codeChallenge = codeVerifier
```

**Note :** Moins sécurisé, éviter en production.

## Implémentation dans cette application

### Frontend (Angular)

Configuration dans `auth-config.service.ts` :

```typescript
const authConfig: AuthConfig = {
  // ... autres paramètres
  responseType: 'code',
  useCodeChallengeMethod: 'S256', // Active PKCE avec SHA-256
};
```

La bibliothèque `angular-oauth2-oidc` gère automatiquement :
- La génération du code verifier
- La génération du code challenge
- L'envoi du challenge dans la requête d'authorization
- L'envoi du verifier dans la requête de token exchange

### Backend (FastAPI)

Le backend n'a pas besoin de modifications spéciales pour PKCE. Keycloak gère automatiquement la validation de PKCE.

### Keycloak Configuration

Dans les paramètres avancés du client :

1. Allez dans **Clients** > Votre client
2. Ouvrez **Advanced settings**
3. Configurez **PKCE Code Challenge Method** : `S256`
4. Keycloak validera automatiquement les requêtes PKCE

## Avantages de PKCE

### Sécurité Renforcée

✅ Protection contre les attaques par interception  
✅ Pas de secret client nécessaire  
✅ Recommandé pour les clients publics  
✅ Conforme aux recommandations de sécurité OAuth 2.0  

### Standards et Best Practices

✅ **RFC 7636** : Standard PKCE (2015)  
✅ **OWASP** : Recommande PKCE pour les SPA  
✅ **OAuth 2.0 Security Best Current Practice** : Recommande PKCE pour tous les clients publics  
✅ **FAPI (Financial-grade API)** : Requiert PKCE pour les clients publics  

### Autres Avantages

✅ Facile à implémenter (support natif par les bibliothèques)  
✅ Pas d'impact sur l'expérience utilisateur  
✅ Compatible avec les flux OAuth 2.0 standard  
✅ Peut être combiné avec d'autres mesures de sécurité  

## Dépannage

### Problème : "Invalid code verifier"

**Cause :** Le code verifier ne correspond pas au code challenge  
**Solution :**
- Vérifiez que `useCodeChallengeMethod` est configuré dans le frontend
- Vérifiez la configuration PKCE dans Keycloak
- Assurez-vous que le même client est utilisé pour l'authorization et le token exchange

### Problème : PKCE non supporté

**Cause :** Keycloak n'a pas PKCE activé  
**Solution :**
1. Allez dans **Clients** > Votre client
2. Ouvrez **Advanced settings**
3. Activez **PKCE Code Challenge Method**

### Problème : code_challenge_method must be S256 or plain

**Cause :** Keycloak supporte seulement S256 ou plain  
**Solution :** Vérifiez que vous utilisez `S256` ou `plain` dans la configuration

## Ressources

- [RFC 7636 - PKCE](https://tools.ietf.org/html/rfc7636)
- [OAuth 2.0 Security Best Practices](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics)
- [angular-oauth2-oidc PKCE Documentation](https://github.com/manfredsteyer/angular-oauth2-oidc)
- [Keycloak PKCE Support](https://www.keycloak.org/docs/latest/securing_apps/#_oidc_pkce)


