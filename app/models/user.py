from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base  # ✅ Vérifie le chemin d'import selon ta structure

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(150), unique=True, index=True, nullable=False)  # Taille 150, à adapter
    hashed_password = Column(String(256), nullable=False)  # Taille adaptée à un hash

    # Relations
    reviews = relationship("Review", back_populates="user", cascade="all, delete")
    user_books = relationship("UserBook", back_populates="user", cascade="all, delete")
