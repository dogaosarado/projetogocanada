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
from app.deps import get_db, get_current_user
from app.models.request import Application, ConsultancyRequest
from app.models.user import User
from app.schemas.relatorio import RelatorioSignupCreate, RelatorioAddServiceCreate
from app.services.email import send_relatorio_client_email, send_request_email


router = APIRouter(prefix="/relatorio", tags=["relatorio"])

@router.post("/adicionar-servico", status_code=201)
def adicionar_servico_relatorio(
    body: RelatorioSignupCreate,  # reusa o mesmo schema — email/name/password do body são ignorados/não usados aqui
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    ja_tem = db.query(ConsultancyRequest).filter(
        ConsultancyRequest.user_id == current_user.id,
        ConsultancyRequest.service_type == "relatorio",
    ).first()
    if ja_tem:
        raise HTTPException(status_code=409, detail="Você já tem um relatório contratado.")

    try:
        body.validate_against_tier()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    db_request = ConsultancyRequest(
        user_id=current_user.id,
        service_type="relatorio",
        tier=body.tier.value,
        universities_selected=[u.model_dump() for u in body.universities_selected],
        research_interests=None,
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
    return {"message": "Relatório adicionado à sua conta."}


@router.get("/meus-servicos")
def meus_servicos(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    tipos = {
        r.service_type for r in
        db.query(ConsultancyRequest.service_type)
        .filter(ConsultancyRequest.user_id == current_user.id)
        .distinct()
    }
    return {"servicos": sorted(tipos)}

@router.post("/signup", status_code=201)
def relatorio_signup(body: RelatorioSignupCreate, db: Session = Depends(get_db)):
    try:
        body.validate_against_tier()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    exists = db.query(User).filter(User.email == body.email).first()
    if exists:
        ja_tem_relatorio = db.query(ConsultancyRequest).filter(
        ConsultancyRequest.user_id == exists.id,
        ConsultancyRequest.service_type == "relatorio",
    ).first()
    if ja_tem_relatorio:
        raise HTTPException(status_code=409, detail="Você já tem relatório contratado.")
    raise HTTPException(
        status_code=409,
        detail="Você já tem conta em outro serviço. Faça login e contrate o relatório no seu painel.",
    )

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

@router.post("/adicionar-servico", status_code=201)
def adicionar_servico_relatorio(
    body: RelatorioAddServiceCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    ja_tem = db.query(ConsultancyRequest).filter(
        ConsultancyRequest.user_id == current_user.id,
        ConsultancyRequest.service_type == "relatorio",
    ).first()
    if ja_tem:
        raise HTTPException(status_code=409, detail="Você já tem um relatório contratado.")

    try:
        body.validate_against_tier()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    db_request = ConsultancyRequest(
        user_id=current_user.id,
        service_type="relatorio",
        tier=body.tier.value,
        universities_selected=[u.model_dump() for u in body.universities_selected],
        research_interests=None,
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
    return {"message": "Relatório adicionado à sua conta."}


@router.get("/meus-servicos")
def meus_servicos(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    tipos = {
        r.service_type for r in
        db.query(ConsultancyRequest.service_type)
        .filter(ConsultancyRequest.user_id == current_user.id)
        .distinct()
    }
    return {"servicos": sorted(tipos)}