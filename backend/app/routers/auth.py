# app/routers/auth.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import create_access_token, verify_password
from app.deps import get_db
from app.exceptions import CredentialsException
from app.models.user import User
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.user import UserResponse
from app.deps import get_active_user


router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/me", response_model=UserResponse)
def me(user: User = Depends(get_active_user)):
    return user

@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == body.email).first()

    if user is None or not verify_password(body.password, user.hashed_password):
        raise CredentialsException()

    if not user.is_active:
        raise CredentialsException()

    token = create_access_token(subject=user.email)
    return TokenResponse(access_token=token)