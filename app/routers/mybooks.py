"""
Ce module définit les routes API pour gérer les livres ajoutés par les utilisateurs.

- POST /userbooks/ : permet à un utilisateur d'ajouter un livre à sa collection personnelle.

Utilise SQLAlchemy pour la gestion de la base de données et FastAPI pour exposer l'API.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import userbook as userbook_schema
from app.models import userbook as userbook_model
from app.database import get_db

router = APIRouter(prefix="/userbooks", tags=["userbooks"])

@router.post("/", response_model=userbook_schema.UserBookOut)
def add_userbook(userbook: userbook_schema.UserBookCreate, db: Session = Depends(get_db)):
    """
    Ajoute un nouveau livre à la collection d'un utilisateur.

    - userbook : données du livre à ajouter (id du livre, id de l'utilisateur, statut).
    - db : session de la base de données.

    Retourne l'objet UserBook créé.
    """
    new_userbook = userbook_model.UserBook(**userbook.dict())
    db.add(new_userbook)
    db.commit()
    db.refresh(new_userbook)
    return new_userbook
