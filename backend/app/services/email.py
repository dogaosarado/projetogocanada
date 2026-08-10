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


# ---------------------------------------------------------------------------
# Mentoria (fluxo com conta/usuário — sem mudança de comportamento)
# ---------------------------------------------------------------------------

def send_mentoria_client_email(user: User, temp_password: str) -> None:
    tier_value = user.tier.value if hasattr(user.tier, "value") else user.tier
    tier_label = MENTORSHIP_TIER_LABELS.get(tier_value, tier_value)

    resend.Emails.send({
        "from": "GoCanadaBR <contato@gocanadabr.com.br>",
        "to": user.email,
        "subject": "Cadastro de mentoria recebido — GoCanadaBR",
        "html": f"""
        <h2>Olá, {user.name}!</h2>
        <p>Seu cadastro no plano de mentoria <strong>{tier_label}</strong> foi recebido.</p>
        <p>Você já pode acessar a plataforma com os dados abaixo:</p>
        <p><strong>Email:</strong> {user.email}<br>
        <strong>Senha temporária:</strong> {temp_password}</p>
        <p>No primeiro acesso você deve trocar essa senha por uma de sua escolha.</p>
        <p>As instruções de pagamento chegam em um email de acompanhamento.</p>
        <p><a href="https://www.gocanadabr.com.br/login">Acessar GoCanadaBR</a></p>
        <br>
        <p>Equipe GoCanadaBR</p>
        """,
    })


def send_payment_link_email(user: User, pix_link: str) -> None:
    """Fluxo de mentoria — depende de User/conta existente."""
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
        <p>Assim que o pagamento for identificado, confirmamos no sistema e entraremos
        em contato para o primeiro encontro.</p>
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


# ---------------------------------------------------------------------------
# Relatório
# ---------------------------------------------------------------------------

def send_relatorio_client_email(user: User, temp_password: str) -> None:
    tier_value = user.tier.value if hasattr(user.tier, "value") else user.tier
    tier_label = TIER_LABELS.get(tier_value, tier_value)

    resend.Emails.send({
        "from": "GoCanadaBR <contato@gocanadabr.com.br>",
        "to": user.email,
        "subject": "Cadastro de relatório recebido — GoCanadaBR",
        "html": f"""
        <h2>Olá, {user.name}!</h2>
        <p>Seu cadastro no plano de relatório <strong>{tier_label}</strong> foi recebido.</p>
        <p>Você já pode acessar a plataforma com os dados abaixo:</p>
        <p><strong>Email:</strong> {user.email}<br>
        <strong>Senha temporária:</strong> {temp_password}</p>
        <p>No primeiro acesso você deve trocar essa senha por uma de sua escolha.</p>
        <p>As instruções de pagamento chegam em um email de acompanhamento.</p>
        <p><a href="https://www.gocanadabr.com.br/login">Acessar GoCanadaBR</a></p>
        <br>
        <p>Equipe GoCanadaBR</p>
        """,
    })

def send_relatorio_interest_pending_payment_email(name: str, email: str, tier: str) -> None:
    """1º email pro cliente: confirma o pedido e avisa que o pagamento
    ainda está pendente — o link de pagamento vem depois, manualmente."""
    tier_label = TIER_LABELS.get(tier, tier)
    price = TIER_PRICES.get(tier, "")

    resend.Emails.send({
        "from": "GoCanadaBR <contato@gocanadabr.com.br>",
        "to": email,
        "subject": "Recebemos seu pedido — pagamento pendente — GoCanadaBR",
        "html": f"""
        <h2>Olá, {name}!</h2>
        <p>Recebemos seu pedido de relatório — plano <strong>{tier_label}</strong> ({price}).</p>
        <p>Em breve você recebe por email o link para pagamento via Pix. Assim que o
        pagamento for confirmado, o relatório é preparado e enviado por email em
        até 48 horas.</p>
        <br>
        <p>Equipe GoCanadaBR</p>
        """,
    })


def send_relatorio_interest_notification_email(
    name: str,
    email: str,
    tier: str,
    universities_selected: list[dict],
    lattes_url: str | None,
) -> None:
    """Email pro consultor com o pedido inteiro, incluindo os links de
    cada departamento — é o que faltava na versão anterior (a função
    duplicada que sobrescrevia essa nunca incluía url nenhuma)."""
    tier_label = TIER_LABELS.get(tier, tier)

    universities_html = "".join(
        f"""<li>
            <strong>{sel.get('university', '')}</strong> — {sel.get('department', '')}
            {f'<br/><a href="{sel["url"]}">{sel["url"]}</a>' if sel.get('url') else ''}
            {' (departamento personalizado, sem link)' if sel.get('is_custom') and not sel.get('url') else ''}
        </li>"""
        for sel in universities_selected
    )
    lattes_html = (
        f'<p><strong>Lattes:</strong> <a href="{lattes_url}">{lattes_url}</a></p>'
        if lattes_url
        else ""
    )

    resend.Emails.send({
        "from": "GoCanadaBR <contato@gocanadabr.com.br>",
        "to": settings.consultant_email,
        "subject": f"[GoCanadaBR] Novo interesse em relatório — {name} ({tier_label})",
        "html": f"""
        <h2>Novo pedido de relatório</h2>
        <p><strong>Nome:</strong> {name}</p>
        <p><strong>Email:</strong> {email}</p>
        <p><strong>Plano:</strong> {tier_label}</p>
        <p><strong>Universidades e departamentos:</strong></p>
        <ul>{universities_html}</ul>
        {lattes_html}
        """,
    })


def send_relatorio_payment_link_email(name: str, email: str, tier: str, pix_link: str) -> None:
    """Disparado manualmente pelo admin (sem User/conta por trás) depois
    de olhar o email de notificação acima."""
    tier_label = TIER_LABELS.get(tier, tier)
    price = TIER_PRICES.get(tier, "")

    resend.Emails.send({
        "from": "GoCanadaBR <contato@gocanadabr.com.br>",
        "to": email,
        "subject": f"Pagamento — Plano {tier_label} — GoCanadaBR",
        "html": f"""
        <h2>Olá, {name}!</h2>
        <p>Segue o link para pagamento via Pix referente ao seu plano
        <strong>{tier_label}</strong> ({price}).</p>
        <p><a href="{pix_link}">{pix_link}</a></p>
        <p>Assim que o pagamento for identificado, seu relatório é preparado e
        enviado por email em até 48 horas.</p>
        <br>
        <p>Equipe GoCanadaBR</p>
        """,
    })


def send_relatorio_report_incoming_email(name: str, email: str) -> None:
    """Disparado manualmente pelo admin depois de confirmar o Pix na conta."""
    resend.Emails.send({
        "from": "GoCanadaBR <contato@gocanadabr.com.br>",
        "to": email,
        "subject": "Pagamento confirmado — seu relatório está a caminho — GoCanadaBR",
        "html": f"""
        <h2>Olá, {name}!</h2>
        <p>Confirmamos o pagamento. Você vai receber o relatório por email em até
        <strong>48 horas</strong>.</p>
        <br>
        <p>Equipe GoCanadaBR</p>
        """,
    })
