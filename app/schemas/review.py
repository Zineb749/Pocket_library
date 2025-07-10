"""
Schémas Pydantic pour gérer les avis (reviews) sur les livres.

Ces classes définissent la structure des données attendues lors de la création
d'un avis, ainsi que la structure des données retournées par l'API.
"""

from pydantic import BaseModel
from typing import Optional

class ReviewCreate(BaseModel):
    """
    Schéma pour créer un nouvel avis.

    Contient l'identifiant du livre, de l'utilisateur, la note et un commentaire optionnel.
    """
    book_id: int
    user_id: int
    rating: int  # Note attribuée au livre (ex : nombre d'étoiles)
    comment: Optional[str] = None  # Commentaire optionnel

class ReviewOut(BaseModel):
    """
    Schéma de sortie pour un avis.

    Représente un avis complet renvoyé au client.
    """
    id: int
    book_id: int
    user_id: int
    rating: int
    comment: Optional[str]

    class Config:
        # Permet la conversion automatique depuis un objet ORM (ex: SQLAlchemy)
        orm_mode = True
