# Fichier : models/user.py
# Ce fichier définit le modèle User pour la base de données.
# Il permet de gérer les utilisateurs de l’application, avec leurs identifiants
# et leurs relations avec les livres et les avis.


from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base 

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(150), unique=True, index=True, nullable=False)
    hashed_password = Column(String(256), nullable=False) 

    # Relations
    reviews = relationship("Review", back_populates="user", cascade="all, delete")
    user_books = relationship("UserBook", back_populates="user", cascade="all, delete")
