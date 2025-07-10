"""
Schémas Pydantic pour la gestion des données liées aux livres.

Ces classes définissent les structures attendues pour les requêtes et réponses
dans l'API, assurant la validation et la sérialisation des données.
"""

from pydantic import BaseModel
from typing import Optional
from datetime import date

class BookPreview(BaseModel):
    """
    Schéma pour afficher un aperçu d'un livre.

    Utilisé lorsque seules certaines informations du livre sont nécessaires,
    comme dans une liste ou un résumé.
    """
    title: str
    author: str
    description: Optional[str] = None
    purchase_date: Optional[date] = None
    cover_url: Optional[str] = None

class BookCreate(BaseModel):
    """
    Schéma pour la création d'un nouveau livre.

    Contient les champs nécessaires lors de l'ajout d'un livre via l'API.
    """
    title: str
    author: str
    description: Optional[str] = None
    purchase_date: Optional[date] = None
    status: Optional[str] = "a_lire"  # Statut par défaut "à lire"
    source: Optional[str] = "manual"  # Source par défaut "manuelle"

class BookOut(BaseModel):
    """
    Schéma de sortie pour un livre.

    Définit la structure des données renvoyées au client lors de la récupération d'un livre.
    """
    id: int
    title: str
    author: str
    description: Optional[str]
    purchase_date: Optional[date]
    status: str
    source: str

    class Config:
        
        from_attributes = True
