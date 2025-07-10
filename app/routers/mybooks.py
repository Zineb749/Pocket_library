from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import userbook as userbook_schema
from app.models import userbook as userbook_model
from app.database import get_db

router = APIRouter(prefix="/userbooks", tags=["userbooks"])

@router.post("/", response_model=userbook_schema.UserBookOut)
def add_userbook(userbook: userbook_schema.UserBookCreate, db: Session = Depends(get_db)):
    new_userbook = userbook_model.UserBook(**userbook.dict())
    db.add(new_userbook)
    db.commit()
    db.refresh(new_userbook)
    return new_userbook

