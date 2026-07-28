# app/deps.py

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.security import decode_access_token
from app.exceptions import CredentialsException
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    email = decode_access_token(token)
    if email is None:
        raise CredentialsException()

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise CredentialsException()

    return user


def get_active_user(user: User = Depends(get_current_user)) -> User:
    # nota: "is_active" agora representa apenas "pagamento confirmado" e não
    # bloqueia mais o acesso do usuário — conta é utilizável assim que criada.
    return user


def get_admin_user(user: User = Depends(get_current_user)) -> User:
    # por ora admin é qualquer usuário com tier avançado
    # depois você pode adicionar um campo is_admin no model
    if user.tier.value != "avancado":
        raise CredentialsException()
    return user