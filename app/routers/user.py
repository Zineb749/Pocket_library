"""
Module API pour la gestion des utilisateurs.

Fonctionnalités principales :
- Création d'un nouvel utilisateur avec mot de passe hashé.
- Route de test pour vérifier le fonctionnement du routeur.

Utilise FastAPI pour définir les routes, SQLAlchemy pour la gestion des données, 
et Passlib pour le hachage des mots de passe.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.schemas import user as user_schema
from app.models import user as user_model
from app.database import get_db

# Création du routeur sans prefix pour éviter /users/users/
router = APIRouter(tags=["users"])

# Configuration du contexte pour le hashage des mots de passe avec bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    """
    Hash le mot de passe en clair en utilisant bcrypt.
    """
    return pwd_context.hash(password)

@router.post("/", response_model=user_schema.UserOut)
def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    """
    Crée un nouvel utilisateur.

    Vérifie que le nom d'utilisateur n'existe pas déjà.
    Hash le mot de passe avant de le stocker.
    Enregistre l'utilisateur en base de données.

    Renvoie l'utilisateur créé (sans mot de passe).
    """
    db_user = db.query(user_model.User).filter(user_model.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    new_user = user_model.User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/test")
async def test():
    """
    Route de test simple pour vérifier que le routeur fonctionne.
    """
    return {"message": "Route users fonctionne !"}
