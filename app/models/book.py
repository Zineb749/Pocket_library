# Fichier : models/book.py
# Ce fichier définit le modèle Book (livre) pour la base de données.
# Il représente un livre que l'utilisateur peut voir, ajouter ou classer.
# Contient aussi les relations avec les avis (reviews) et les livres de l'utilisateur (UserBook).


from sqlalchemy import Column, Integer, String, Text, Date
from sqlalchemy.orm import relationship
from app.database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    author = Column(String(255))
    description = Column(Text, nullable=True)
    purchase_date = Column(Date, nullable=True)
    cover_url = Column(String(255), nullable=True)

    status = Column(String(50), default="a_lire", nullable=False)
    source = Column(String(50), default="manual", nullable=False) 

    reviews = relationship("Review", back_populates="book")
    user_books = relationship("UserBook", back_populates="book")
