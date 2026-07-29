# pages/landing.py

from nicegui import ui
from pages.layout import brand_logo
from services.api import create_lead, get_posts
import re


def _excerpt(html: str, max_len: int = 110) -> str:
    text = re.sub(r"<[^>]+>", " ", html or "")
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > max_len:
        return text[:max_len].rsplit(" ", 1)[0] + "…"
    return text


TIERS = [
    {
        "name": "Básico",
        "price": "R$ 250",
        "tier_key": "basico",
        "features": [
            "2 universidades",
            "1 departamento por universidade",
            "Dossiê para o processo seletivo",
            "Tuition e valor da bolsa",
        ],
    },
    {
        "name": "Intermediário",
        "price": "R$ 400",
        "tier_key": "intermediario",
        "features": [
            "3 universidades",
            "1 departamento por universidade",
            "Tudo do plano Básico",
            "Ficha de 1 professor por departamento",
            "Artigos, orientações e temas de pesquisa",
        ],
        "highlight": True,
    },
    {
        "name": "Avançado",
        "price": "R$ 800",
        "tier_key": "avancado",
        "features": [
            "4 universidades",
            "1 departamento por universidade",
            "Tudo do plano Intermediário",
            "Ficha de 2 professores por departamento",
            "Desconto em consultoria personalizada",
        ],
    },
]


STEPS = [
    {
        "image": "/assets/step1.jpg",
        "title": "1. Escolha o plano e crie sua conta",
        "desc": "Selecione o plano ideal e cadastre seus dados. Você recebe acesso imediato por email.",
    },
    {
        "image": "/assets/step2.jpg",
        "title": "2. Conheça a plataforma e peça seu relatório",
        "desc": "Explore o painel e preencha o formulário com as universidades e programas de seu interesse.",
    },
    {
        "image": "/assets/step3.jpg",
        "title": "3. Pague o plano escolhido",
        "desc": "Você recebe as instruções de pagamento por email e confirma o pagamento do plano.",
    },
    {
        "image": "/assets/step4.jpg",
        "title": "4. Receba seu relatório",
        "desc": "Com o relatório em mãos, decida se quer seguir com a mentoria personalizada.",
    },
]


def landing_page() -> None:
    selected_tier = {"value": None}

    with ui.column().classes("w-full min-h-screen bg-stone-50"):

        # header
        with ui.row().classes("w-full px-8 py-5 bg-white shadow-sm justify-between items-center"):
            brand_logo()
            with ui.row().classes("gap-3 items-center"):
                ui.button("Quem somos", on_click=lambda: ui.navigate.to("/quem-somos")).props(
                    "flat color=amber"
                )
                ui.button("Blog", on_click=lambda: ui.navigate.to("/blog")).props("flat color=amber")
                ui.button("Entrar", on_click=lambda: ui.navigate.to("/login")).classes(
                    "bg-amber-600 text-white rounded-xl px-5 py-2 hover:bg-amber-700"
                )

        # hero
        with ui.column().classes("w-full items-center py-20 px-4 text-center"):
            ui.label("Sua pós-graduação no Canadá").classes(
                "text-4xl font-bold text-stone-800 mb-4"
            )
            ui.label(
                "Pesquisa especializada sobre universidades, programas e professores "
                "para que você possa focar no que importa: sua candidatura."
            ).classes("text-stone-500 text-lg max-w-xl mb-10")
            ui.button(
                "Ver planos",
                on_click=lambda: ui.run_javascript(
                    "document.getElementById('planos').scrollIntoView({behavior:'smooth'})"
                ),
            ).classes("bg-amber-600 text-white rounded-xl px-8 py-3 text-lg hover:bg-amber-700")

        # como funciona
        with ui.column().classes("w-full items-center py-16 px-4 bg-white"):
            ui.label("Como funciona").classes("text-3xl font-bold text-stone-800 mb-10 text-center")
            with ui.row().classes("gap-6 flex-wrap justify-center max-w-5xl"):
                for step in STEPS:
                    with ui.column().classes("w-56 items-center text-center gap-3"):
                        ui.image(step["image"]).classes(
                            "w-full h-36 rounded-2xl object-cover shadow-sm bg-stone-100"
                        )
                        ui.label(step["title"]).classes("text-stone-800 font-semibold")
                        ui.label(step["desc"]).classes("text-stone-500 text-sm")

        # tiers
        with ui.column().classes("w-full items-center py-16 px-4 bg-white").props('id="planos"'):
            ui.label("Escolha seu plano").classes("text-3xl font-bold text-stone-800 mb-2 text-center")
            ui.label(
                "Selecione o plano ideal e preencha seus dados para começar."
            ).classes("text-stone-500 mb-10 text-center")

            with ui.row().classes("gap-6 flex-wrap justify-center"):
                tier_select_ref = {"widget": None}
                for tier in TIERS:
                    highlight = tier.get("highlight", False)
                    card_classes = (
                        "w-72 p-6 rounded-2xl shadow-md flex flex-col gap-3 border-2 border-amber-500 bg-amber-50"
                        if highlight
                        else "w-72 p-6 rounded-2xl shadow-md flex flex-col gap-3 bg-stone-50"
                    )
                    with ui.card().classes(card_classes):
                        if highlight:
                            ui.label("Mais popular").classes(
                                "text-xs font-bold text-amber-700 bg-amber-100 px-3 py-1 rounded-full self-start"
                            )
                        ui.label(tier["name"]).classes("text-xl font-bold text-stone-800")
                        ui.label(tier["price"]).classes("text-3xl font-bold text-amber-700")

                        ui.separator()

                        for feature in tier["features"]:
                            ui.html(f'<div style="display:flex; align-items:flex-start; gap:8px; margin-bottom:4px;"><span style="color:#d97706; flex-shrink:0; margin-top:2px;">✓</span><span style="color:#57534e; font-size:0.875rem; line-height:1.4;">{feature}</span></div>')

                        ui.space()

                        def make_handler(t=tier["tier_key"]):
                            def handler():
                                selected_tier["value"] = t
                                if tier_select_ref["widget"]:
                                    tier_select_ref["widget"].value = t
                                ui.run_javascript(
                                    "document.getElementById('cadastro').scrollIntoView({behavior:'smooth'})"
                                )
                            return handler

                        ui.button(
                            "Quero este plano",
                            on_click=make_handler(),
                        ).classes("w-full mt-2 bg-amber-600 text-white rounded-xl py-2 hover:bg-amber-700")

        # formulário de interesse
        with ui.column().classes("w-full items-center py-16 px-4").props('id="cadastro"'):
            ui.label("Comece agora").classes("text-3xl font-bold text-stone-800 mb-2 text-center")
            ui.label(
                "Preencha seus dados e entraremos em contato com suas credenciais de acesso."
            ).classes("text-stone-500 mb-8 text-center")

            with ui.card().classes("w-full max-w-md p-8 shadow-lg rounded-2xl bg-white"):
                name_input = ui.input("Nome completo").classes("w-full")
                email_input = ui.input("Email").classes("w-full mt-3")

                tier_select = ui.select(
                    {"basico": "Básico — R$ 250", "intermediario": "Intermediário — R$ 400", "avancado": "Avançado — R$ 800"},
                    label="Plano",
                    value="basico",
                ).classes("w-full mt-3")
                tier_select_ref["widget"] = tier_select

                error_msg = ui.label("").classes("text-red-500 text-sm mt-2")
                error_msg.set_visibility(False)

                def handle_interest():
                    if not name_input.value.strip():
                        error_msg.text = "Informe seu nome."
                        error_msg.set_visibility(True)
                        return
                    if not email_input.value.strip():
                        error_msg.text = "Informe seu email."
                        error_msg.set_visibility(True)
                        return

                    tier_val = selected_tier["value"] or tier_select.value
                    result = create_lead(name_input.value, email_input.value, tier_val)
                    if result:
                        ui.navigate.to("/interesse")
                    else:
                        error_msg.text = "Erro ao cadastrar. Tente novamente."
                        error_msg.set_visibility(True)

                ui.button("Enviar", on_click=handle_interest).classes(
                    "w-full mt-6 bg-amber-600 text-white rounded-xl py-2 hover:bg-amber-700"
                )

        # novidades — 3 posts mais recentes do blog
        posts = get_posts()[:3]
        if posts:
            with ui.column().classes("w-full items-center py-16 px-4"):
                ui.label("Novidades").classes("text-3xl font-bold text-stone-800 mb-8 text-center")
                with ui.row().classes("gap-6 flex-wrap justify-center max-w-4xl"):
                    for post in posts:
                        data_fmt = post["created_at"][:10] if post.get("created_at") else ""
                        with ui.card().classes(
                            "w-72 p-6 rounded-2xl shadow-sm bg-white cursor-pointer hover:shadow-md transition-all"
                        ).on("click", lambda slug=post["slug"]: ui.navigate.to(f"/blog/{slug}")):
                            ui.label(data_fmt).classes("text-xs text-amber-600 font-medium mb-1")
                            ui.label(post["title"]).classes("text-stone-800 font-semibold mb-2")
                            ui.label(_excerpt(post.get("body_html", ""))).classes(
                                "text-stone-500 text-sm mb-2"
                            )
                            ui.button("Ler mais →").props("flat color=amber").classes("px-0")

        # footer
        with ui.row().classes("w-full px-8 py-6 bg-stone-800 justify-center"):
            ui.label("© 2026 GoCanada — Todos os direitos reservados").classes("text-stone-400 text-sm")