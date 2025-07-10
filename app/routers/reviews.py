from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import review as review_schema
from app.models import review as review_model
from app.database import get_db

router = APIRouter(prefix="/reviews", tags=["reviews"])

@router.post("/", response_model=review_schema.ReviewOut)
def create_review(review: review_schema.ReviewCreate, db: Session = Depends(get_db)):
    new_review = review_model.Review(**review.dict())
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review

