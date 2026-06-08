# app/routers/requests.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.deps import get_active_user, get_db
from app.exceptions import TierPermissionException
from app.models.request import ConsultancyRequest
from app.models.user import User
from app.schemas.request import RequestCreate, RequestResponse
from app.services.email import send_request_email

router = APIRouter(prefix="/requests", tags=["requests"])


@router.post("", response_model=RequestResponse, status_code=201)
def create_request(
    body: RequestCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_active_user),
):
    try:
        body.validate_against_tier(user.tier)
    except ValueError:
        raise TierPermissionException()

    db_request = ConsultancyRequest(
        user_id=user.id,
        tier=user.tier.value,
        universities_selected=[
            u.model_dump() for u in body.universities_selected
        ],
        research_interests=body.research_interests,
    )

    db.add(db_request)
    db.commit()
    db.refresh(db_request)

    send_request_email(user=user, request=db_request)

    return db_request