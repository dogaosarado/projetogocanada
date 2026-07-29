# app/services/email.py

import resend

from app.core.config import settings
from app.models.request import ConsultancyRequest
from app.models.user import User

resend.api_key = settings.resend_api_key


def _build_email_body(user: User, request: ConsultancyRequest) -> str:
    universities_block = ""
    for selection in request.universities_selected:
        custom_label = " (personalizada)" if selection.get("is_custom") else ""
        university = selection.get("university", "")
        department = selection.get("department", "")
        url = selection.get("url", "")

        url_html = f'<br/><a href="{url}">{url}</a>' if url else ""

        universities_block += f"""
        <li>
            <strong>{university}{custom_label}</strong><br/>
            Programa: {department}{url_html}
        </li>
        """

    research_block = (
        f"<p><strong>Interesses de pesquisa:</strong> {request.research_interests}</p>"
        if request.research_interests
        else ""
    )

    return f"""
    <h2>Novo pedido de consultoria</h2>

    <h3>Cliente</h3>
    <p><strong>Email:</strong> {user.email}</p>
    <p><strong>Plano:</strong> {request.tier}</p>

    <h3>Universidades selecionadas</h3>
    <ul>
        {universities_block}
    </ul>

    {research_block}
    """


TIER_LABELS = {
    "basico": "Básico",
    "intermediario": "Intermediário",
    "avancado": "Avançado",
}

TIER_PRICES = {
    "basico": "R$ 250",
    "intermediario": "R$ 400",
    "avancado": "R$ 800",
}


def send_payment_link_email(user: User, pix_link: str) -> None:
    tier_value = user.tier.value if hasattr(user.tier, "value") else user.tier
    tier_label = TIER_LABELS.get(tier_value, tier_value)
    price = TIER_PRICES.get(tier_value, "")

    resend.Emails.send({
        "from": "GoCanadaBR <contato@gocanadabr.com.br>",
        "to": user.email,
        "subject": f"Pagamento — Plano {tier_label} — GoCanadaBR",
        "html": f"""
        <h2>Olá!</h2>
        <p>Segue o link para pagamento via Pix referente ao seu plano
        <strong>{tier_label}</strong> ({price}).</p>
        <p><a href="{pix_link}">{pix_link}</a></p>
        <p>Assim que o pagamento for identificado, confirmamos no sistema e seu
        relatório entra em preparação.</p>
        <p>Qualquer dúvida, é só responder este email.</p>
        <br>
        <p>Equipe GoCanadaBR</p>
        """,
    })


def send_request_email(user: User, request: ConsultancyRequest) -> None:
    body = _build_email_body(user, request)

    resend.Emails.send({
        "from": "GoCanadaBR <contato@gocanadabr.com.br>",
        "to": settings.consultant_email,
        "subject": f"[GoCanadaBR] Novo pedido — {user.email} ({request.tier})",
        "html": body,
    })