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


def send_request_email(user: User, request: ConsultancyRequest) -> None:
    body = _build_email_body(user, request)

    resend.Emails.send({
        "from": "GoCanadaBR <contato@gocanadabr.com.br>",
        "to": settings.consultant_email,
        "subject": f"[GoCanadaBR] Novo pedido — {user.email} ({request.tier})",
        "html": body,
    })