# pages/relatorio.py
#
# Página do produto "relatório" (avulso). Renomeado de landing.py — o nome
# antigo não fazia sentido: essa página nunca foi a home, é a home
# (mentoria.py, rota "/") que enviava tráfego pra cá via botão "Relatórios".
#
# Oferece SÓ o relatório. Mentoria não aparece aqui — quem quer mentoria
# já está em "/" antes de chegar nesta página.
#
# Paleta/fontes/header/footer vêm de pages/layout.py.

from nicegui import ui
from pages.layout import design_tokens, site_header, site_footer
from services.api import create_lead, get_posts
import re


def _excerpt(html: str, max_len: int = 110) -> str:
    text = re.sub(r"<[^>]+>", " ", html or "")
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > max_len:
        return text[:max_len].rsplit(" ", 1)[0] + "…"
    return text


# ---------------------------------------------------------------------------
# Relatórios (serviço avulso — tier gratuito + 3 pagos)
# ---------------------------------------------------------------------------
TIERS = [
    {
        "name": "Grátis",
        "price": "0",
        "tier_key": "relatorio_gratis",
        "features": [
            "1 universidade",
            "1 departamento",
            "Tuition e valor da bolsa",
        ],
    },
    {
        "name": "Básico",
        "price": "150",
        "tier_key": "relatorio_basico",
        "features": [
            "2 universidades",
            "1 departamento por universidade",
            "Dossiê para o processo seletivo",
            "Tuition e valor da bolsa",
            "Levantamento dos grupos de pesquisa do departamento",
        ],
    },
    {
        "name": "Intermediário",
        "price": "250",
        "tier_key": "relatorio_intermediario",
        "features": [
            "3 universidades",
            "1 departamento por universidade",
            "Dossiê para o processo seletivo",
            "Tuition e valor da bolsa",
            "Levantamento dos grupos de pesquisa dos departamentos",
        ],
        "highlight": True,
    },
    {
        "name": "Avançado",
        "price": "400",
        "tier_key": "relatorio_avancado",
        "features": [
            "4 universidades",
            "1 departamento por universidade",
            "Dossiê para o processo seletivo",
            "Tuition e valor da bolsa",
            "Levantamento dos grupos de pesquisa do departamento",
            "20% de desconto na mentoria",
        ],
    },
]


WHAT_IS_HIGHLIGHTS = [
    {
        "title": "Fontes oficiais",
        "desc": "Dados coletados direto dos sites das universidades, departamentos e programas — não de agregadores ou blogs.",
    },
    {
        "title": "Curadoria e organização",
        "desc": "As informações são checadas e organizadas num único documento, sem versões contraditórias ou desatualizadas.",
    },
    {
        "title": "Seu tempo em outra coisa",
        "desc": "Enquanto o relatório resolve o levantamento, você foca no que exige a sua atenção: carta de motivação, contato com professores, documentação.",
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


def _tier_cards(tiers: list[dict], scroll_target_id: str, select_ref: dict) -> None:
    """Renders a row of pricing cards."""
    with ui.row().classes("gap-6 flex-wrap justify-center"):
        for tier in tiers:
            highlight = tier.get("highlight", False)
            card_classes = (
                "w-72 p-6 rounded-none flex flex-col gap-3 bg-[#F5F0E6] "
                "border-2 border-[#A6402F]"
                if highlight
                else "w-72 p-6 rounded-none flex flex-col gap-3 bg-[#F5F0E6]"
            )
            with ui.card().classes(card_classes):
                if highlight:
                    ui.label("MAIS POPULAR").classes(
                        "text-[10px] font-mono tracking-widest text-[#F5F0E6] "
                        "bg-[#A6402F] px-3 py-1 self-start"
                    )
                ui.label(tier["name"]).classes(
                    "font-display text-xl font-semibold text-[#16233D] mt-1"
                )
                with ui.row().classes("items-baseline gap-1"):
                    ui.label("R$").classes("font-mono text-sm text-[#A6402F]")
                    ui.label(tier["price"]).classes(
                        "font-mono text-3xl font-medium text-[#A6402F]"
                    )

                ui.element("div").classes("h-px w-full bg-[#B8925A55] my-2")

                for feature in tier["features"]:
                    with ui.row().classes("items-start gap-2"):
                        ui.label("✓").classes(
                            "text-[#A6402F] font-mono text-sm flex-shrink-0"
                        )
                        ui.label(feature).classes(
                            "text-[#4B5563] text-sm leading-snug"
                        )

                ui.space()

                def make_handler(t=tier["tier_key"]):
                    def handler():
                        select_ref["value"] = t
                        if select_ref.get("widget"):
                            select_ref["widget"].value = t
                        ui.run_javascript(
                            f"document.getElementById('{scroll_target_id}').scrollIntoView({{behavior:'smooth'}})"
                        )
                    return handler

                ui.button(
                    "Quero este plano",
                    on_click=make_handler(),
                ).classes(
                    "w-full mt-2 bg-[#16233D] text-[#F5F0E6] rounded-none py-2 "
                    "font-mono text-xs tracking-wide hover:bg-[#0f182b]"
                )


def relatorio_page() -> None:
    design_tokens()
    selected_tier = {"value": None}

    with ui.column().classes("w-full min-h-screen bg-[#F5F0E6] font-body"):

        site_header("relatorio")

        # hero
        with ui.column().classes("w-full items-center py-20 px-4 text-center"):
            ui.label("Sua pós-graduação no Canadá").classes(
                "font-display text-4xl font-semibold text-[#16233D] mb-4"
            )
            ui.label(
                "Pesquisa especializada sobre universidades, programas e professores "
                "para que você possa focar no que importa: sua candidatura."
            ).classes("text-[#4B5563] text-lg max-w-xl mb-10")
            ui.button(
                "Ver planos",
                on_click=lambda: ui.run_javascript(
                    "document.getElementById('planos').scrollIntoView({behavior:'smooth'})"
                ),
            ).classes(
                "bg-[#A6402F] text-[#F5F0E6] rounded-none px-8 py-3 text-lg "
                "font-mono text-sm tracking-wide hover:bg-[#8a3327]"
            )

        # o que é
        with ui.column().classes("w-full items-center py-16 px-4"):
            ui.label("O que é o relatório").classes(
                "font-display text-3xl font-semibold text-[#16233D] mb-4 text-center"
            )
            ui.label(
                "Um levantamento completo sobre as universidades e programas do seu interesse: "
                "prazos de seleção, requisitos, valores de tuition, bolsas disponíveis e os "
                "professores cujas linhas de pesquisa fazem sentido para você. Tudo levantado "
                "em fontes oficiais, curado e organizado — para que a decisão de onde aplicar "
                "não dependa de garimpar dezenas de páginas em inglês."
            ).classes("text-[#4B5563] text-base max-w-2xl mb-10 text-center")

            with ui.row().classes("gap-6 flex-wrap justify-center max-w-5xl"):
                for item in WHAT_IS_HIGHLIGHTS:
                    with ui.column().classes(
                        "w-64 gap-2 p-6 bg-white border border-[#B8925A55] rounded-none"
                    ):
                        ui.label(item["title"]).classes(
                            "font-mono text-xs tracking-widest text-[#A6402F] uppercase"
                        )
                        ui.label(item["desc"]).classes(
                            "text-[#4B5563] text-sm leading-snug"
                        )

        # como funciona
        with ui.column().classes("w-full items-center py-16 px-4 bg-white"):
            ui.label("Como funciona").classes(
                "font-display text-3xl font-semibold text-[#16233D] mb-10 text-center"
            )
            with ui.row().classes("gap-6 flex-wrap justify-center max-w-5xl"):
                for step in STEPS:
                    with ui.column().classes("w-56 items-center text-center gap-3"):
                        ui.image(step["image"]).classes(
                            "w-full h-36 rounded-none object-cover shadow-sm bg-[#F5F0E6]"
                        )
                        ui.label(step["title"]).classes(
                            "text-[#16233D] font-semibold"
                        )
                        ui.label(step["desc"]).classes("text-[#4B5563] text-sm")

        # tiers (relatórios)
        with ui.column().classes(
            "w-full items-center py-16 px-4 bg-white"
        ).props('id="planos"'):
            ui.label("Escolha seu plano de relatório").classes(
                "font-display text-3xl font-semibold text-[#16233D] mb-2 text-center"
            )
            ui.label(
                "Selecione o plano ideal e preencha seus dados para começar."
            ).classes("text-[#4B5563] mb-10 text-center font-mono text-sm")

            tier_select_ref = {"widget": None, "value": None}
            _tier_cards(TIERS, "cadastro", tier_select_ref)
            selected_tier = tier_select_ref

        # formulário de interesse
        with ui.column().classes(
            "w-full items-center py-16 px-4"
        ).props('id="cadastro"'):
            ui.label("Comece agora").classes(
                "font-display text-3xl font-semibold text-[#16233D] mb-2 text-center"
            )
            ui.label(
                "Preencha seus dados e entraremos em contato com suas credenciais de acesso."
            ).classes("text-[#4B5563] mb-8 text-center")

            with ui.card().classes(
                "w-full max-w-md p-8 rounded-none shadow-md bg-white"
            ):
                name_input = ui.input("Nome completo").classes("w-full")
                email_input = ui.input("Email").classes("w-full mt-3")

                tier_select = ui.select(
                    {
                        "relatorio_gratis": "Grátis",
                        "relatorio_basico": "Básico — R$ 150",
                        "relatorio_intermediario": "Intermediário — R$ 250",
                        "relatorio_avancado": "Avançado — R$ 400",
                    },
                    label="Plano",
                    value="relatorio_gratis",
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
                    "w-full mt-6 bg-[#A6402F] text-[#F5F0E6] rounded-none py-2 "
                    "font-mono text-sm tracking-wide hover:bg-[#8a3327]"
                )

        # novidades — 3 posts mais recentes do blog
        posts = get_posts()[:3]
        if posts:
            with ui.column().classes("w-full items-center py-16 px-4"):
                ui.label("Novidades").classes(
                    "font-display text-3xl font-semibold text-[#16233D] mb-8 text-center"
                )
                with ui.row().classes("gap-6 flex-wrap justify-center max-w-4xl"):
                    for post in posts:
                        data_fmt = post["created_at"][:10] if post.get("created_at") else ""
                        with ui.card().classes(
                            "w-72 p-6 rounded-none shadow-sm bg-white cursor-pointer "
                            "hover:shadow-md transition-all"
                        ).on(
                            "click",
                            lambda slug=post["slug"]: ui.navigate.to(f"/blog/{slug}"),
                        ):
                            ui.label(data_fmt).classes(
                                "text-xs text-[#A6402F] font-mono mb-1"
                            )
                            ui.label(post["title"]).classes(
                                "text-[#16233D] font-semibold mb-2"
                            )
                            ui.label(_excerpt(post.get("body_html", ""))).classes(
                                "text-[#4B5563] text-sm mb-2"
                            )
                            ui.button("Ler mais →").props("flat").classes(
                                "text-[#A6402F] font-mono text-xs px-0"
                            )

        site_footer()
