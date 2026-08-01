# app/routers/mentoria.py

import secrets

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.deps import get_db
from app.models.request import Application, ConsultancyRequest
from app.models.user import User
from app.schemas.mentoria import MentoriaSignupCreate
from app.services.email import send_mentoria_client_email, send_request_email

router = APIRouter(prefix="/mentoria", tags=["mentoria"])


@router.post("/signup", status_code=201)
def mentoria_signup(body: MentoriaSignupCreate, db: Session = Depends(get_db)):
    try:
        body.validate_against_tier()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    exists = db.query(User).filter(User.email == body.email).first()
    if exists:
        raise HTTPException(status_code=409, detail="Email já cadastrado.")

    temp_password = secrets.token_urlsafe(12)

    db_user = User(
        email=body.email,
        name=body.name,
        hashed_password=hash_password(temp_password),
        tier=body.tier,
        is_active=False,  # mesmo padrão do Pix atual: ativa na confirmação manual do pagamento
        must_change_password=True,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    db_request = ConsultancyRequest(
        user_id=db_user.id,
        tier=body.tier.value,
        universities_selected=[u.model_dump() for u in body.universities_selected],
        research_interests=body.research_interests,
    )
    db.add(db_request)
    db.commit()
    db.refresh(db_request)

    for selection in body.universities_selected:
        db.add(Application(
            user_id=db_user.id,
            request_id=db_request.id,
            university=selection.university,
            department=selection.department,
            url=selection.url,
            is_custom=selection.is_custom,
        ))
    db.commit()

    send_mentoria_client_email(db_user, temp_password)
    send_request_email(user=db_user, request=db_request)  # já genérico, não precisa mudar

    return {"message": "Cadastro realizado. Você já pode acessar a plataforma."}