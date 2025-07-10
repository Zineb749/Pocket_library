from pydantic import BaseModel
from typing import Optional

class UserBookCreate(BaseModel):
    book_id: int
    user_id: int
    status: Optional[str] = "a lire"

class UserBookOut(BaseModel):
    id: int
    book_id: int
    user_id: int
    status: str

    class Config:
        orm_mode = True
