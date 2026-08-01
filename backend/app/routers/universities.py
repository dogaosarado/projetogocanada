# app/routers/universities.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.deps import get_db
from app.models.university import University
from app.schemas.university import UniversityResponse

router = APIRouter(prefix="/universities", tags=["universities"])


@router.get("", response_model=list[UniversityResponse])
def list_universities(db: Session = Depends(get_db)):
    return db.query(University).order_by(University.name).all()