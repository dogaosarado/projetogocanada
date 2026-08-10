# app/routers/relatorio_signup.py
#
# Cria User de verdade pro produto "relatório". Antes disso, pages/relatorio_signup.py
# chamava submit_relatorio_interest() -> POST /relatorio/interesse, que é o
# router de LEAD: sem User, sem senha, sem checagem de email duplicado. Isso
# aqui é o que faltava, espelhando app/routers/mentoria.py.

import secrets

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.deps import get_db
from app.models.request import Application, ConsultancyRequest
from app.models.user import User
from app.schemas.relatorio import RelatorioSignupCreate
from app.services.email import send_relatorio_client_email, send_request_email

router = APIRouter(prefix="/relatorio", tags=["relatorio"])


@router.post("/signup", status_code=201)
def relatorio_signup(body: RelatorioSignupCreate, db: Session = Depends(get_db)):
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
        is_active=False,
        must_change_password=True,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    db_request = ConsultancyRequest(
        user_id=db_user.id,
        tier=body.tier.value,
        universities_selected=[u.model_dump() for u in body.universities_selected],
        research_interests=None,
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

    send_relatorio_client_email(db_user, temp_password)
    send_request_email(user=db_user, request=db_request)

    return {"message": "Cadastro realizado. Você já pode acessar a plataforma."}