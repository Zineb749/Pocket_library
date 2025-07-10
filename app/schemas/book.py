from pydantic import BaseModel
from typing import Optional
from datetime import date

class BookPreview(BaseModel):
    title: str
    author: str
    description: Optional[str] = None
    purchase_date: Optional[date] = None
    cover_url: Optional[str] = None

class BookCreate(BaseModel):
    title: str
    author: str
    description: Optional[str] = None
    purchase_date: Optional[date] = None
    status: Optional[str] = "a_lire"   # valeurs possibles: 'a_lire', 'en_cours', 'lu'
    source: Optional[str] = "manual"   # 'manual' ou 'google_books'

class BookOut(BaseModel):
    id: int
    title: str
    author: str
    description: Optional[str]
    purchase_date: Optional[date]
    status: str
    source: str

    class Config:
        from_attributes = True  # pour que Pydantic prenne les attributs d'un ORM comme SQLAlchemy

