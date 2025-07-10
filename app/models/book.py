from sqlalchemy import Column, Integer, String, Text, Date
from sqlalchemy.orm import relationship
from app.database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)             # longueur fixée à 255
    author = Column(String(255))                         # longueur fixée à 255
    description = Column(Text, nullable=True)
    purchase_date = Column(Date, nullable=True)
    cover_url = Column(String(255), nullable=True)      # longueur fixée à 255

    status = Column(String(50), default="a_lire", nullable=False)   # longueur 50, suffisant pour ce champ
    source = Column(String(50), default="manual", nullable=False)  # longueur 50

    reviews = relationship("Review", back_populates="book")
    user_books = relationship("UserBook", back_populates="book")
