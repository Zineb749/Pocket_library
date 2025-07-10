# Fichier : models/userbook.py
# Ce fichier définit le modèle UserBook qui représente la relation entre un utilisateur
# et un livre. Il permet de suivre les livres ajoutés par l'utilisateur et leur statut
# de lecture (à lire, lu, en cours de lecture).

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class UserBook(Base):
    __tablename__ = "user_books"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String(20), default="a_lire", nullable=False)

    book = relationship("Book", back_populates="user_books")
    user = relationship("User", back_populates="user_books")
