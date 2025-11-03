# Démarrage Rapide

## 1. Démarrer Keycloak

```bash
docker-compose up -d
```

Attendez quelques secondes puis vérifiez : http://localhost:8080

## 2. Configurer Keycloak

1. Allez sur http://localhost:8080
2. Cliquez sur **Administration Console**
3. Connectez-vous avec `admin` / `admin`
4. Créez un client :
   - **Clients** > **Create client**
   - **Client ID**: `angular-client`
   - **Client authentication**: OFF (Public client)
   - **Valid redirect URIs**: `http://localhost:4200/*`
   - **Valid post logout redirect URIs**: `http://localhost:4200/*`
   - **Web origins**: `*`
   - Dans **Advanced settings** : **PKCE Code Challenge Method** : `S256`
   - Save

## 3. Démarrer le Backend

```bash
cd backend
pip install -r requirements.txt
./run.sh
```

Backend : http://localhost:8000

## 4. Démarrer le Frontend

```bash
cd frontend
npm install
npm start
```

Frontend : http://localhost:4200

## 5. Tester

1. Ouvrez http://localhost:4200
2. Cliquez **Login**
3. Connectez-vous avec `admin` / `admin`
4. Accédez à **Profile**

## Arrêter Keycloak

```bash
docker-compose down
```

## Documentation Complète

- [README.md](README.md) - Documentation principale
- [KEYCLOAK_SETUP.md](KEYCLOAK_SETUP.md) - Configuration détaillée de Keycloak
- [SETUP.md](SETUP.md) - Guide de configuration complet

