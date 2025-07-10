from pydantic import BaseModel
from typing import Optional

class ReviewCreate(BaseModel):
    book_id: int
    user_id: int
    rating: int  # 1 to 5
    comment: Optional[str] = None

class ReviewOut(BaseModel):
    id: int
    book_id: int
    user_id: int
    rating: int
    comment: Optional[str]

    class Config:
        orm_mode = True
