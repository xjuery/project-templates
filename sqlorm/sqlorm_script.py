from sqlmodel import SQLModel, Field, Relationship, create_engine, Session, select
from typing import List, Optional
from sqlalchemy import Column, Integer, String, Text, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import relationship

# Configuration de la base de données
DATABASE_URL = "sqlite:///./test_database.db"
engine = create_engine(DATABASE_URL, echo=False)

# Table d'association pour la relation many-to-many
class LivreAuteur(SQLModel, table=True):
    __tablename__ = "t03_livres_auteurs"

    id: Optional[int] = Field(default=None, sa_column=Column("t03_id", Integer, primary_key=True))
    livre_id: int = Field(sa_column=Column("t01_id", Integer, ForeignKey("t01_livres.t01_id"), nullable=False))
    auteur_id: int = Field(sa_column=Column("t02_id", Integer, ForeignKey("t02_auteurs.t02_id"), nullable=False))

# Modèle pour les livres
class Livre(SQLModel, table=True):
    __tablename__ = "t01_livres"

    id: Optional[int] = Field(default=None, sa_column=Column("t01_id", Integer, primary_key=True))
    titre: str = Field(default_factory=lambda: "", sa_column=Column("t01_titre", String(255), nullable=False))
    description: Optional[str] = Field(default=None, sa_column=Column("t01_description", Text))

    # Relation many-to-many avec auteurs
    auteurs: List["Auteur"] = Relationship(back_populates="livres", link_model=LivreAuteur)

# Modèle pour les auteurs
class Auteur(SQLModel, table=True):
    __tablename__ = "t02_auteurs"

    id: Optional[int] = Field(default=None, sa_column=Column("t02_id", Integer, primary_key=True))
    prenom: str = Field(default_factory=lambda: "", sa_column=Column("t02_prenom", String(100), nullable=False))
    nom: str = Field(default_factory=lambda: "", sa_column=Column("t02_nom", String(100), nullable=False))
    biographie: Optional[str] = Field(default=None, sa_column=Column("t02_biographie", Text))

    # Relation many-to-many avec livres
    livres: List[Livre] = Relationship(back_populates="auteurs", link_model=LivreAuteur)

# Fonctions CRUD pour les livres
def create_livre(session: Session, titre: str, description: Optional[str] = None) -> Livre:
    livre = Livre(titre=titre, _description=description)
    session.add(livre)
    session.commit()
    session.refresh(livre)
    return livre

def read_livres(session: Session) -> List[Livre]:
    return session.exec(select(Livre)).all()

def read_livre_by_id(session: Session, livre_id: int) -> Optional[Livre]:
    return session.exec(select(Livre).where(Livre.id == livre_id)).first()

def update_livre(session: Session, livre_id: int, titre: Optional[str] = None, description: Optional[str] = None) -> Optional[Livre]:
    livre = session.exec(select(Livre).where(Livre.id == livre_id)).first()
    if livre:
        if titre:
            livre.titre = titre
        if description is not None:
            livre.description = description
        session.commit()
        session.refresh(livre)
    return livre

def delete_livre(session: Session, livre_id: int) -> bool:
    livre = session.exec(select(Livre).where(Livre.id == livre_id)).first()
    if livre:
        session.delete(livre)
        session.commit()
        return True
    return False

# Fonctions CRUD pour les auteurs
def create_auteur(session: Session, prenom: str, nom: str, biographie: Optional[str] = None) -> Auteur:
    auteur = Auteur(prenom=prenom, nom=nom, biographie=biographie)
    session.add(auteur)
    session.commit()
    session.refresh(auteur)
    return auteur

def read_auteurs(session: Session) -> List[Auteur]:
    return session.exec(select(Auteur)).all()

def read_auteur_by_id(session: Session, auteur_id: int) -> Optional[Auteur]:
    return session.exec(select(Auteur).where(Auteur.id == auteur_id)).first()

def update_auteur(session: Session, auteur_id: int, prenom: Optional[str] = None, nom: Optional[str] = None, biographie: Optional[str] = None) -> Optional[Auteur]:
    auteur = session.exec(select(Auteur).where(Auteur.id == auteur_id)).first()
    if auteur:
        if prenom:
            auteur.prenom = prenom
        if nom:
            auteur.nom = nom
        if biographie is not None:
            auteur.biographie = biographie
        session.commit()
        session.refresh(auteur)
    return auteur

def delete_auteur(session: Session, auteur_id: int) -> bool:
    auteur = session.exec(select(Auteur).where(Auteur.id == auteur_id)).first()
    if auteur:
        session.delete(auteur)
        session.commit()
        return True
    return False

# Fonctions pour gérer la relation many-to-many
def add_auteur_to_livre(session: Session, livre_id: int, auteur_id: int) -> bool:
    livre = session.exec(select(Livre).where(Livre.id == livre_id)).first()
    auteur = session.exec(select(Auteur).where(Auteur.id == auteur_id)).first()
    if livre and auteur:
        # Vérifier si la relation existe déjà
        existing = session.exec(select(LivreAuteur).where(
            LivreAuteur.livre_id == livre_id,
            LivreAuteur.auteur_id == auteur_id
        )).first()
        if not existing:
            association = LivreAuteur(livre_id=livre_id, auteur_id=auteur_id)
            session.add(association)
            session.commit()
            return True
    return False

def remove_auteur_from_livre(session: Session, livre_id: int, auteur_id: int) -> bool:
    association = session.exec(select(LivreAuteur).where(
        LivreAuteur.livre_id == livre_id,
        LivreAuteur.auteur_id == auteur_id
    )).first()
    if association:
        session.delete(association)
        session.commit()
        return True
    return False

# Fonction pour créer les tables
def create_tables():
    SQLModel.metadata.create_all(engine)

# Fonction pour obtenir une session
def get_session():
    return Session(engine)

if __name__ == "__main__":
    # Créer les tables
    create_tables()

    # Tester avec des données exemple
    with get_session() as session:
        # Créer des auteurs
        auteur1 = create_auteur(session, "Victor", "Hugo", "Écrivain français célèbre.")
        auteur2 = create_auteur(session, "Albert", "Camus", "Philosophe et écrivain français.")
        auteur3 = create_auteur(session, "John", "Doe", "Unknown author.")
        auteur4 = create_auteur(session, "Jane", "Doe", "Also uknown author.")

        # Créer des livres
        livre1 = create_livre(session, "Les Misérables", "Roman historique de Victor Hugo.")
        livre2 = create_livre(session, "L'Étranger", "Roman philosophique d'Albert Camus.")
        livre3 = create_livre(session, "Book 3", "New book 3.")
        livre4 = create_livre(session, "Book 4", "New book 4.")

        # Associer auteurs aux livres
        add_auteur_to_livre(session, livre1.id, auteur1.id)
        add_auteur_to_livre(session, livre3.id, auteur1.id)
        add_auteur_to_livre(session, livre2.id, auteur2.id)
        add_auteur_to_livre(session, livre2.id, auteur3.id)
        add_auteur_to_livre(session, livre2.id, auteur4.id)

        # Lire et afficher
        livres = read_livres(session)
        for livre in livres:
            print(f"Livre: {livre.titre} - Auteurs: {[f'{a.prenom} {a.nom}' for a in livre.auteurs]}")

        auteurs = read_auteurs(session)
        for auteur in auteurs:
            print(f"Auteur: {auteur.prenom} {auteur.nom} - Livres: {[l.titre for l in auteur.livres]}")