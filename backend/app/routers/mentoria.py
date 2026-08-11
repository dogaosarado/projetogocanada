# app/routers/mentoria.py

import secrets

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.request import Application, ConsultancyRequest
from app.models.user import User
from app.services.email import send_mentoria_client_email, send_request_email
from app.deps import get_db, get_current_user
from app.schemas.mentoria import MentoriaSignupCreate, MentoriaAddServiceCreate
router = APIRouter(prefix="/mentoria", tags=["mentoria"])


@router.post("/signup", status_code=201)
def mentoria_signup(body: MentoriaSignupCreate, db: Session = Depends(get_db)):
    try:
        body.validate_against_tier()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    exists = db.query(User).filter(User.email == body.email).first()
    if exists:
        ja_tem_mentoria = db.query(ConsultancyRequest).filter(
        ConsultancyRequest.user_id == exists.id,
        ConsultancyRequest.service_type == "mentoria",
    ).first()
    if ja_tem_mentoria:
        raise HTTPException(status_code=409, detail="Você já tem mentoria contratada.")
    raise HTTPException(
        status_code=409,
        detail="Você já tem conta em outro serviço. Faça login e contrate a mentoria no seu painel.",
    )

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
    service_type="mentoria",  # ADICIONAR
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

@router.post("/adicionar-servico", status_code=201)
def adicionar_servico_mentoria(
    body: MentoriaAddServiceCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    ja_tem = db.query(ConsultancyRequest).filter(
        ConsultancyRequest.user_id == current_user.id,
        ConsultancyRequest.service_type == "mentoria",
    ).first()
    if ja_tem:
        raise HTTPException(status_code=409, detail="Você já tem mentoria contratada.")

    try:
        body.validate_against_tier()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    db_request = ConsultancyRequest(
        user_id=current_user.id,
        service_type="mentoria",
        tier=body.tier.value,
        universities_selected=[u.model_dump() for u in body.universities_selected],
        research_interests=body.research_interests,
    )
    db.add(db_request)
    db.commit()
    db.refresh(db_request)

    for selection in body.universities_selected:
        db.add(Application(
            user_id=current_user.id,
            request_id=db_request.id,
            university=selection.university,
            department=selection.department,
            url=selection.url,
            is_custom=selection.is_custom,
        ))
    db.commit()

    send_request_email(user=current_user, request=db_request)
    return {"message": "Mentoria adicionada à sua conta."}