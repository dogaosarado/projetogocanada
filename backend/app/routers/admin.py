# app/routers/admin.py

from app.models.user import TierEnum
from app.models import user
import resend
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.security import hash_password
from app.deps import get_admin_user, get_db
from app.exceptions import NotFoundException
from app.models.user import User
from app.schemas.user import UserResponse, UserTierUpdate
from app.schemas.auth import LoginRequest
from pydantic import EmailStr
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from app.models.content import Meeting, Deadline
from app.schemas.content import MeetingCreate, MeetingResponse, DeadlineCreate, DeadlineResponse
from app.models.request import ConsultancyRequest
from app.models.content import Meeting, Deadline, ChecklistProgress

router = APIRouter(prefix="/admin", tags=["admin"])


class UserCreate(LoginRequest):
    tier: str

class LeadCreate(BaseModel):
    name: str
    email: EmailStr
    tier: str

@router.post("/leads", status_code=201)
def create_lead(body: LeadCreate, db: Session = Depends(get_db)):
    from app.core.security import hash_password
    from app.models.user import TierEnum
    import secrets

    exists = db.query(User).filter(User.email == body.email).first()
    if exists:
        raise HTTPException(status_code=409, detail="Email já cadastrado.")

    temp_password = secrets.token_urlsafe(12)

    db_user = User(
        email=body.email,
        name=body.name,
        hashed_password=hash_password(temp_password),
        tier=TierEnum(body.tier),
        is_active=False,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    import resend
    from app.core.config import settings
    resend.api_key = settings.resend_api_key
    resend.Emails.send({
    "from": "GoCanadaBR <contato@gocanadabr.com.br>",
    "to": body.email,
    "subject": "Recebemos seu cadastro — GoCanadaBR",
    "html": f"""
    <h2>Olá, {body.name}!</h2>
    <p>Recebemos seu interesse no plano <strong>{body.tier}</strong>.</p>
    <p>Em breve você receberá um email com suas credenciais de acesso para preencher o formulário de universidades e programas.</p>
    <p>Qualquer dúvida, responda este email.</p>
    <br>
    <p>Equipe GoCanadaBR</p>
    """
})
    resend.Emails.send({
        "from": "GoCanadaBR <contato@gocanadabr.com.br>",
        "to": settings.consultant_email,
        "subject": f"[GoCanadaBR] Novo interesse — {body.name} ({body.tier})",
        "html": f"""
        <h2>Novo cliente interessado</h2>
        <p><strong>Nome:</strong> {body.name}</p>
        <p><strong>Email:</strong> {body.email}</p>
        <p><strong>Plano:</strong> {body.tier}</p>
        <p>Acesse o painel admin para ativar a conta após confirmação do pagamento.</p>
        <p><strong>Senha temporária:</strong> {temp_password}</p>
        """
    })

    return {"message": "Cadastro realizado. Entraremos em contato em breve."}

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

@router.post("/users/{user_id}/meetings", response_model=MeetingResponse, status_code=201)
def add_meeting(user_id: int, body: MeetingCreate, db: Session = Depends(get_db), _: User = Depends(get_admin_user)):
    meeting = Meeting(user_id=user_id, **body.model_dump())
    db.add(meeting)
    db.commit()
    db.refresh(meeting)
    return meeting

@router.post("/users/{user_id}/deadlines", response_model=DeadlineResponse, status_code=201)
def add_deadline(user_id: int, body: DeadlineCreate, db: Session = Depends(get_db), _: User = Depends(get_admin_user)):
    deadline = Deadline(user_id=user_id, **body.model_dump())
    db.add(deadline)
    db.commit()
    db.refresh(deadline)
    return deadline

@router.delete("/users/{user_id}", status_code=204)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_admin_user),
):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise NotFoundException("Usuário")

    db.query(ConsultancyRequest).filter(ConsultancyRequest.user_id == user_id).delete()
    db.query(Meeting).filter(Meeting.user_id == user_id).delete()
    db.query(Deadline).filter(Deadline.user_id == user_id).delete()
    db.query(ChecklistProgress).filter(ChecklistProgress.user_id == user_id).delete()

    db.delete(user)
    db.commit()

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

    import resend
    from app.core.config import settings
    resend.api_key = settings.resend_api_key

    resend.Emails.send({
    "from": "GoCanada <contato@gocanadabr.com.br>",
    "to": user.email,
    "subject": "Sua conta GoCanadaBR está ativa!",
    "html": f"""
    <h2>Sua conta foi ativada!</h2>
    <p>Seu plano <strong>{user.tier.value}</strong> está ativo.</p>
    <p>Acesse o link abaixo para fazer login:</p>
    <p><a href="https://www.gocanadabr.com.br/login">Acessar GoCanadaBR</a></p>
    <p><strong>Email:</strong> {user.email}</p>
    <p><strong>Senha:</strong> use a senha que você recebeu no email de cadastro inicial.</p>
    <p>Caso não encontre, entre em contato respondendo este email.</p>
    <br>
    <p>Equipe GoCanadaBR</p>
    """
})

    return user