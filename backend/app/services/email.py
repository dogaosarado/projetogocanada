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
    "relatorio_gratis": "Grátis",
    "relatorio_basico": "Básico",
    "relatorio_intermediario": "Intermediário",
    "relatorio_avancado": "Avançado",
}

TIER_PRICES = {
    "relatorio_gratis": "R$ 0",
    "relatorio_basico": "R$ 150",
    "relatorio_intermediario": "R$ 250",
    "relatorio_avancado": "R$ 400",
}

# Mentoria é produto separado do relatório — mesmos nomes de tier ("basico"
# etc.), preços muito diferentes. Se send_payment_link_email() for reaproveitada
# pra cobrar mentoria, ela vai pegar o preço errado daqui. Ver aviso no chat.
MENTORSHIP_TIER_LABELS = {
    "mentoria_basico": "Básico",
    "mentoria_intermediario": "Intermediário",
    "mentoria_avancado": "Avançado",
}

MENTORSHIP_TIER_PRICES = {
    "mentoria_basico": "R$ 1.500",
    "mentoria_intermediario": "R$ 2.000",
    "mentoria_avancado": "R$ 3.000",
}


def send_payment_link_email(user: User, pix_link: str) -> None:
    tier_value = user.tier.value if hasattr(user.tier, "value") else user.tier
    all_labels = {**TIER_LABELS, **MENTORSHIP_TIER_LABELS}
    all_prices = {**TIER_PRICES, **MENTORSHIP_TIER_PRICES}
    tier_label = all_labels.get(tier_value, tier_value)
    price = all_prices.get(tier_value, "")

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
        relatório entra em preparação. Ele será enviado em até 48 horas após o recebimento do pagamento.</p>
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