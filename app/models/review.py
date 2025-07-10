from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base  # Vérifie le chemin d'import si besoin

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    rating = Column(Integer, nullable=False)  # Exemple : 1 à 5
    comment = Column(String(500), nullable=True)  # Taille 500 choisie, à adapter selon besoin

    # Relations
    book = relationship("Book", back_populates="reviews")
    user = relationship("User", back_populates="reviews")
