from datetime import datetime
from pydantic import BaseModel, EmailStr
from app.models.user import TierEnum
from typing import Optional

class UserTierUpdate(BaseModel):
    tier: TierEnum


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    tier: TierEnum
    is_active: bool
    name: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}