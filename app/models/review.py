# Fichier : models/review.py
# Ce fichier définit le modèle Review (avis) pour la base de données.
# Il permet aux utilisateurs de laisser une note (sous forme d’étoiles) et un commentaire sur un livre.
# Chaque avis est lié à un livre et un utilisateur.

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(String(500), nullable=True) 


    book = relationship("Book", back_populates="reviews")
    user = relationship("User", back_populates="reviews")
