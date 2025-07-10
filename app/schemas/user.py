"""
Schémas Pydantic pour la gestion des utilisateurs.

Ces classes définissent la structure des données pour la création d'un utilisateur
et la structure des données retournées lors de la récupération d'un utilisateur.
"""

from pydantic import BaseModel

class UserCreate(BaseModel):
    """
    Schéma pour la création d'un nouvel utilisateur.

    Contient les champs nécessaires pour l'inscription d'un utilisateur.
    """
    username: str
    password: str

class UserOut(BaseModel):
    """
    Schéma de sortie pour un utilisateur.

    Définit les données renvoyées au client, sans exposer le mot de passe.
    """
    id: int
    username: str

    class Config:
        # Permet la conversion automatique depuis un objet ORM (ex: SQLAlchemy)
        orm_mode = True
