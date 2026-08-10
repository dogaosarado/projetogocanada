# app/routers/relatorio.py
#
# Endpoint público do fluxo de "relatório". Propositalmente SEM banco de dados:
# o pedido não é persistido em lugar nenhum, só dispara dois emails (cliente +
# consultor). Antes isso vivia em app/routers/admin.py como create_lead() —
# só que havia DUAS funções create_lead() no mesmo arquivo com o mesmo nome;
# a segunda sobrescrevia a primeira, então a versão que incluía os links de
# departamento no email do consultor nunca rodava de verdade. Também faltava
# `from pydantic import field_validator`, o que quebraria a rota na primeira
# vez que alguém tentasse validar. Ambos os bugs são resolvidos aqui.

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr, field_validator

from app.services.email import (
    send_relatorio_interest_pending_payment_email,
    send_relatorio_interest_notification_email,
)

router = APIRouter(prefix="/relatorio", tags=["relatorio"])

REPORT_UNIVERSITY_LIMITS = {
    "relatorio_gratis": 1,
    "relatorio_basico": 2,
    "relatorio_intermediario": 3,
    "relatorio_avancado": 4,
}


class UniversitySelection(BaseModel):
    university: str
    department: str
    url: str | None = None
    is_custom: bool = False


class RelatorioInterest(BaseModel):
    name: str
    email: EmailStr
    tier: str
    universities_selected: list[UniversitySelection]
    lattes_url: str | None = None

    @field_validator("universities_selected")
    @classmethod
    def at_least_one_university(cls, v):
        if not v:
            raise ValueError("Selecione ao menos uma universidade.")
        return v

    def validate_against_tier(self) -> None:
        limit = REPORT_UNIVERSITY_LIMITS.get(self.tier)
        if limit is None:
            raise ValueError("Tier inválido.")
        if len(self.universities_selected) > limit:
            raise ValueError(f"Seu plano permite no máximo {limit} universidade(s).")


@router.post("/interesse", status_code=201)
def submit_relatorio_interest(body: RelatorioInterest):
    """Sem persistência: valida, envia email de 'pagamento pendente' pro
    cliente e email de notificação (com os links de departamento) pro
    consultor. Se o Resend falhar, devolve 502 — não há nada salvo pra
    reprocessar depois, então o cliente precisa saber na hora que falhou."""
    try:
        body.validate_against_tier()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    universities_dicts = [u.model_dump() for u in body.universities_selected]

    try:
        send_relatorio_interest_pending_payment_email(body.name, body.email, body.tier)
        send_relatorio_interest_notification_email(
            body.name, body.email, body.tier, universities_dicts, body.lattes_url
        )
    except Exception as e:
        print(f"relatorio interest email send failed: {e}")
        raise HTTPException(status_code=502, detail="Erro ao enviar pedido. Tente novamente.")

    return {"message": "Pedido enviado. Você vai receber um email de confirmação em instantes."}
