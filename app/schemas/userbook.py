
"""
Schémas Pydantic pour la gestion des livres liés aux utilisateurs.

Ces classes définissent la structure des données pour l'ajout d'un livre à un utilisateur
et pour la réponse envoyée lors de la récupération d'un livre utilisateur.
"""

from pydantic import BaseModel
from typing import Optional

class UserBookCreate(BaseModel):
    """
    Schéma pour créer une entrée livre-utilisateur.

    Contient l'ID du livre, l'ID de l'utilisateur et le statut de lecture du livre.
    Le statut par défaut est "a lire".
    """
    book_id: int
    user_id: int
    status: Optional[str] = "a lire"

class UserBookOut(BaseModel):
    """
    Schéma de sortie pour une entrée livre-utilisateur.

    Renvoie l'ID de l'entrée, l'ID du livre, l'ID de l'utilisateur et le statut.
    """
    id: int
    book_id: int
    user_id: int
    status: str

    class Config:
        # Permet la conversion automatique depuis un objet ORM (ex: SQLAlchemy)
        orm_mode = True
