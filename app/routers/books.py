"""
Ce module définit les routes API pour gérer les livres dans l'application.

- GET /books/ : permet de rechercher des livres avec des filtres optionnels (titre, auteur, statut).
- POST /books/ : permet d'ajouter un nouveau livre dans la base de données.

Utilise SQLAlchemy pour interagir avec la base de données et FastAPI pour exposer ces fonctionnalités via une API REST.
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.book import Book
from app.schemas.book import BookCreate, BookOut

router = APIRouter(tags=["books"])  # Prefix supprimé ici

@router.get("/", response_model=List[BookOut])
def search_books(
    title: Optional[str] = Query(None),
    author: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Book)
    if title:
        query = query.filter(Book.title.ilike(f"%{title}%"))
    if author:
        query = query.filter(Book.author.ilike(f"%{author}%"))
    if status:
        query = query.filter(Book.status == status)
    return query.all()

@router.post("/", response_model=BookOut)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    db_book = Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
