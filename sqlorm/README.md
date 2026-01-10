# SQLORM Script

Ce script Python utilise SQLModel et SQLAlchemy pour gérer des objets en base de données SQLite.

## Fonctionnalités

- **Livres** : titre et description
- **Auteurs** : prénom, nom, biographie
- **Relation many-to-many** : un livre peut avoir plusieurs auteurs, un auteur peut avoir écrit plusieurs livres

## Tables

- `t01_livres` : t01_id, t01_titre, t01_description
- `t02_auteurs` : t02_id, t02_prenom, t02_nom, t02_biographie
- `t03_livres_auteurs` : t03_id, t01_id, t02_id

## Installation

1. Installer les dépendances :
   ```
   pip install -r requirements.txt
   ```

## Utilisation

Exécuter le script :
```
python3 sqlorm_script.py
```

Cela créera la base de données `test_database.db`, les tables, insérera des données de test et affichera les résultats.

## Fonctions disponibles

- `create_livre(session, titre, description)` : Créer un livre
- `read_livres(session)` : Lire tous les livres
- `read_livre_by_id(session, id)` : Lire un livre par ID
- `update_livre(session, id, titre, description)` : Modifier un livre
- `delete_livre(session, id)` : Supprimer un livre
- `create_auteur(session, prenom, nom, biographie)` : Créer un auteur
- `read_auteurs(session)` : Lire tous les auteurs
- `read_auteur_by_id(session, id)` : Lire un auteur par ID
- `update_auteur(session, id, prenom, nom, biographie)` : Modifier un auteur
- `delete_auteur(session, id)` : Supprimer un auteur
- `add_auteur_to_livre(session, livre_id, auteur_id)` : Ajouter un auteur à un livre
- `remove_auteur_from_livre(session, livre_id, auteur_id)` : Retirer un auteur d'un livre

## Base de données de test

Le script crée automatiquement une base SQLite `test_database.db` avec des données exemple.