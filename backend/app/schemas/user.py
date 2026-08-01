from datetime import datetime
from pydantic import BaseModel, EmailStr
from app.models.user import TierEnum
from typing import Optional

class UserTierUpdate(BaseModel):
    tier: TierEnum


class PaymentLinkSend(BaseModel):
    pix_link: str


class PasswordChange(BaseModel):
    current_password: str
    new_password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    tier: TierEnum
    is_active: bool
    is_admin: bool
    must_change_password: bool
    name: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}
