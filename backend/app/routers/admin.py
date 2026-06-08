# app/routers/admin.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.deps import get_admin_user, get_db
from app.exceptions import NotFoundException
from app.models.user import User
from app.schemas.user import UserResponse, UserTierUpdate
from app.schemas.auth import LoginRequest

router = APIRouter(prefix="/admin", tags=["admin"])


class UserCreate(LoginRequest):
    tier: str

@router.get("/users", response_model=list[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    _: User = Depends(get_admin_user),
):
    return db.query(User).order_by(User.created_at.desc()).all()

@router.post("/users", response_model=UserResponse, status_code=201)
def create_user(
    body: UserCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_admin_user),
):
    from app.models.user import TierEnum

    db_user = User(
        email=body.email,
        hashed_password=hash_password(body.password),
        tier=TierEnum(body.tier),
        is_active=False,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@router.patch("/users/{user_id}/tier", response_model=UserResponse)
def update_user_tier(
    user_id: int,
    body: UserTierUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_admin_user),
):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise NotFoundException("Usuário")

    user.tier = body.tier
    user.is_active = True

    db.commit()
    db.refresh(user)

    return user