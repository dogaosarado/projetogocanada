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
from app.schemas.user import UserResponse, UserTierUpdate, PaymentLinkSend
from app.services.email import send_payment_link_email
from app.schemas.auth import LoginRequest
from pydantic import EmailStr
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from app.models.content import Meeting, Deadline, ChecklistProgress
from app.schemas.content import MeetingCreate, MeetingResponse, DeadlineCreate, DeadlineResponse
from app.models.request import ConsultancyRequest, Application
from app.schemas.request import ApplicationResponse
router = APIRouter(prefix="/admin", tags=["admin"])


class UserCreate(LoginRequest):
    tier: str

class LeadCreate(BaseModel):
    name: str
    email: EmailStr
    tier: str

@router.post("/leads", status_code=201)
def create_lead(body: LeadCreate):
    from app.core.config import settings
    import resend

    resend.api_key = settings.resend_api_key

    try:
        resend.Emails.send({
            "from": "GoCanadaBR <contato@gocanadabr.com.br>",
            "to": body.email,
            "subject": "Recebemos seu pedido — GoCanadaBR",
            "html": f"""
            <h2>Olá, {body.name}!</h2>
            <p>Recebemos seu pedido para o plano <strong>{body.tier}</strong>.</p>
            <p>Entraremos em contato em breve.</p>
            <br>
            <p>Equipe GoCanadaBR</p>
            """,
        })

        resend.Emails.send({
            "from": "GoCanadaBR <contato@gocanadabr.com.br>",
            "to": settings.consultant_email,
            "subject": f"[GoCanadaBR] Novo pedido — {body.name} ({body.tier})",
            "html": f"""
            <h2>Novo pedido — relatório</h2>
            <p><strong>Nome:</strong> {body.name}</p>
            <p><strong>Email:</strong> {body.email}</p>
            <p><strong>Plano:</strong> {body.tier}</p>
            """,
        })
    except Exception as e:
        print(f"pedido email send failed: {e}")
        raise HTTPException(status_code=502, detail="Erro ao enviar pedido. Tente novamente.")

    return {"message": "Pedido enviado. Entraremos em contato em breve."}
@router.get("/users", response_model=list[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    _: User = Depends(get_admin_user),
):
    return db.query(User).order_by(User.created_at.desc()).all()

@router.get("/users/{user_id}/detail")
def get_user_detail(
    user_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_admin_user),
):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise NotFoundException("Usuário")

    meetings = db.query(Meeting).filter(Meeting.user_id == user_id).order_by(Meeting.scheduled_at).all()
    applications = db.query(Application).filter(Application.user_id == user_id).order_by(Application.created_at).all()

    return {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "tier": user.tier.value,
        "is_active": user.is_active,
        "meetings": [MeetingResponse.model_validate(m) for m in meetings],
        "applications": [ApplicationResponse.model_validate(a) for a in applications],
    }


@router.get("/applications/{application_id}/detail")
def get_application_admin_detail(
    application_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_admin_user),
):
    application = db.query(Application).filter(Application.id == application_id).first()
    if application is None:
        raise NotFoundException("Candidatura")

    deadlines = db.query(Deadline).filter(Deadline.application_id == application_id).order_by(Deadline.due_date).all()

    return {
        "id": application.id,
        "university": application.university,
        "department": application.department,
        "url": application.url,
        "is_custom": application.is_custom,
        "deadlines": [DeadlineResponse.model_validate(d) for d in deadlines],
    }

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

@router.post("/applications/{application_id}/deadlines", response_model=DeadlineResponse, status_code=201)
def add_deadline(application_id: int, body: DeadlineCreate, db: Session = Depends(get_db), _: User = Depends(get_admin_user)):
    application = db.query(Application).filter(Application.id == application_id).first()
    if application is None:
        raise NotFoundException("Candidatura")
    deadline = Deadline(user_id=application.user_id, application_id=application.id, **body.model_dump())
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

    db.query(Meeting).filter(Meeting.user_id == user_id).delete()
    db.query(Deadline).filter(Deadline.user_id == user_id).delete()
    db.query(ChecklistProgress).filter(ChecklistProgress.user_id == user_id).delete()
    db.query(Application).filter(Application.user_id == user_id).delete()
    db.query(ConsultancyRequest).filter(ConsultancyRequest.user_id == user_id).delete()

    db.delete(user)
    db.commit()

@router.post("/users/{user_id}/send-payment-link", status_code=200)
def send_payment_link(
    user_id: int,
    body: PaymentLinkSend,
    db: Session = Depends(get_db),
    _: User = Depends(get_admin_user),
):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise NotFoundException("Usuário")

    send_payment_link_email(user, body.pix_link)

    return {"message": "Link de pagamento enviado."}


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
    "from": "GoCanadaBR <contato@gocanadabr.com.br>",
    "to": user.email,
    "subject": "Pagamento confirmado — GoCanadaBR",
    "html": f"""
    <h2>Recebemos seu pagamento!</h2>
    <p>Confirmamos o pagamento do plano <strong>{user.tier.value}</strong>.</p>
    <p>Nosso consultor já está com seus dados e vai preparar seu relatório em breve.</p>
    <p>Você pode acompanhar tudo no seu painel:</p>
    <p><a href="https://www.gocanadabr.com.br/login">Acessar GoCanadaBR</a></p>
    <p>Qualquer dúvida, é só responder este email.</p>
    <br>
    <p>Equipe GoCanadaBR</p>
    """
})

    return user
