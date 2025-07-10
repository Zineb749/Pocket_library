from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import review as review_schema
from app.models import review as review_model

"""
Ce module gère les routes API liées aux avis (reviews) des utilisateurs sur les livres.

- POST /reviews/ : permet à un utilisateur de créer un nouvel avis sur un livre.

Utilise FastAPI pour définir les routes et SQLAlchemy pour la gestion des données en base.
"""

from app.database import get_db

router = APIRouter(prefix="/reviews", tags=["reviews"])

@router.post("/", response_model=review_schema.ReviewOut)
def create_review(review: review_schema.ReviewCreate, db: Session = Depends(get_db)):
    """
    Crée un nouvel avis utilisateur pour un livre.

    - review : données de l'avis (id du livre, id de l'utilisateur, note, commentaire).
    - db : session de la base de données.

    Retourne l'objet Review créé.
    """
    new_review = review_model.Review(**review.dict())
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review

