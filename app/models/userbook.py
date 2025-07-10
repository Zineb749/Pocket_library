from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base  # ✅ Corrigé

class UserBook(Base):
    __tablename__ = "user_books"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String(20), default="a_lire", nullable=False)  # valeurs possibles : 'lu', 'en_cours', 'a_lire'

    book = relationship("Book", back_populates="user_books")
    user = relationship("User", back_populates="user_books")
