# pages/mentoria.py
#
# Página dedicada à mentoria (produto independente do relatório).
# Conteúdo abaixo é placeholder — subtítulos, texto e bullets marcados com
# TODO são pra você reescrever com a proposta de valor real de cada etapa.

from nicegui import ui
from pages.layout import brand_logo
from services.api import create_lead


# ---------------------------------------------------------------------------
# Mentoria (produto independente do relatório) — vivia em landing.py antes
# do rename pra relatorio.py; movido pra cá porque relatorio.py não deve
# saber nada sobre o produto mentoria.
# ---------------------------------------------------------------------------
MENTORSHIP_TIERS = [
    {
        "name": "Básico",
        "price": "R$ 1.500",
        "tier_key": "mentoria_basico",
        "features": [
            "10 encontros",
            "Agendados conforme sua disponibilidade",
            # TODO: preencher com o escopo real de cada encontro
            "Acompanhamento em dois processos de aplicação",
        ],
    },
    {
        "name": "Intermediário",
        "price": "R$ 2.000",
        "tier_key": "mentoria_intermediario",
        "features": [
            "12 encontros",
            "Agendados conforme sua disponibilidade",
            "Acompanhamento em três processos de aplicação",
            # TODO: preencher com o diferencial deste tier
        ],
        "highlight": True,
    },
    {
        "name": "Avançado",
        "price": "R$ 3.000",
        "tier_key": "mentoria_avancado",
        "features": [
            "14 encontros",
            "Agendados conforme sua disponibilidade",
            "Acompanhamento em quatro processos de aplicação",
            # TODO: preencher com o diferencial deste tier
        ],
    },
]


def mentoria_page() -> None:
    selected_tier = {"value": None}

    with ui.column().classes("w-full min-h-screen bg-stone-50"):

        # header — mesmo padrão da landing
        with ui.row().classes("w-full px-8 py-5 bg-white shadow-sm justify-between items-center"):
            brand_logo()
            with ui.row().classes("gap-3 items-center"):
                ui.button("Relatórios", on_click=lambda: ui.navigate.to("/relatorio")).props(
                    "flat color=amber"
                )
                ui.button("Quem somos", on_click=lambda: ui.navigate.to("/quem-somos")).props(
                    "flat color=amber"
                )
                ui.button("Blog", on_click=lambda: ui.navigate.to("/blog")).props("flat color=amber")
                ui.button("Contato", on_click=lambda: ui.navigate.to("/contato")).props(
                    "flat color=amber"
                )
                ui.button("Entrar", on_click=lambda: ui.navigate.to("/login")).classes(
                    "bg-amber-600 text-white rounded-xl px-5 py-2 hover:bg-amber-700"
                )

        # hero
        with ui.column().classes("w-full items-center py-20 px-4 text-center"):
            ui.label("Mentoria para sua pós-graduação no Canadá").classes(
                "text-4xl font-bold text-stone-800 mb-4"
            )
            # TODO: reescrever — proposta de valor específica da mentoria,
            # diferenciando do relatório avulso.
            ui.label(
                "Acompanhamento individual do início ao fim do processo de aplicação, "
                "com encontros marcados de acordo com a sua agenda."
            ).classes("text-stone-500 text-lg max-w-xl mb-10")
            ui.button(
                "Ver planos",
                on_click=lambda: ui.run_javascript(
                    "document.getElementById('planos-mentoria').scrollIntoView({behavior:'smooth'})"
                ),
            ).classes("bg-amber-600 text-white rounded-xl px-8 py-3 text-lg hover:bg-amber-700")

        # subtítulo 1 — o que é
        with ui.column().classes("w-full items-center py-16 px-4 bg-white"):
            with ui.column().classes("max-w-3xl gap-4"):
                ui.label("O que é a mentoria").classes("text-3xl font-bold text-stone-800 mb-2")
                # TODO: texto real
                ui.label(
                    "A mentoria é composta de reuniões preparatórias para a candidatura. Com elas, você entende o processo seletivo de pós-graduação "
                    "no Canadá em detalhe — editais, prazos, critérios de avaliação, documentação exigida por universidade e "
                    "departamento. A mentoria desmistifica etapas que costumam travar o candidato (carta de motivação, currículo "
                    "acadêmico, contato com potenciais orientadores) e ajuda a organizar ideias e documentos de forma estruturada. "
                    "O objetivo é fazer a candidatura de forma inteligente, com decisões embasadas em cima do seu perfil e objetivos acadêmicos."
                ).classes("text-stone-600 leading-relaxed")

        # subtítulo 2 — para quem é
        with ui.column().classes("w-full items-center py-16 px-4"):
            with ui.column().classes("max-w-3xl gap-4"):
                ui.label("Para quem é").classes("text-3xl font-bold text-stone-800 mb-2")
                ui.html(
                    "<ul style='color:#57534e; line-height:1.6; padding-left:1.2rem;'>"
                    "<li>Para quem decidiu fazer uma pós no Canadá</li>"
                    "<li>Para quem quer realmente entender o processo seletivo</li>"
                    "<li>Para quem quer tomar as melhores decisões durante a aplicação</li>"
                    "</ul>"
                )

        # subtítulo 3 — como funciona (etapas)
        with ui.column().classes("w-full items-center py-16 px-4 bg-white"):
            with ui.column().classes("max-w-3xl gap-4"):
                ui.label("Como funciona").classes("text-3xl font-bold text-stone-800 mb-2")
                ui.html(
                    "<ol style='color:#57534e; line-height:1.6; padding-left:1.2rem;'>"
                    "<li>Os encontros são focados nos seguintes objetivos:</li>"
                    "<li>1- Apresentação da dinâmica de aplicação e alinhamento com a candidatura;</li>"
                    "<li>2- Preparação documental e textual;</li>"
                    "<li>3- Identificação de potenciais departamentos e supervisores;</li>"
                    "<li>4- Estratégias de contato e engajamento.</li>"
                    "</ol>"
                )

        # planos
        with ui.column().classes("w-full items-center py-16 px-4 bg-amber-50/40").props(
            'id="planos-mentoria"'
        ):
            ui.label("Escolha seu plano de mentoria").classes(
                "text-3xl font-bold text-stone-800 mb-2 text-center"
            )
            ui.label(
                "Todos os planos incluem encontros agendados conforme sua disponibilidade."
            ).classes("text-stone-500 mb-10 text-center")

            with ui.row().classes("gap-6 flex-wrap justify-center"):
                tier_select_ref = {"widget": None}
                for tier in MENTORSHIP_TIERS:
                    highlight = tier.get("highlight", False)
                    card_classes = (
                        "w-72 p-6 rounded-2xl shadow-md flex flex-col gap-3 border-2 border-amber-500 bg-white"
                        if highlight
                        else "w-72 p-6 rounded-2xl shadow-md flex flex-col gap-3 bg-white"
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
                            ui.html(
                                f'<div style="display:flex; align-items:flex-start; gap:8px; margin-bottom:4px;">'
                                f'<span style="color:#d97706; flex-shrink:0; margin-top:2px;">✓</span>'
                                f'<span style="color:#57534e; font-size:0.875rem; line-height:1.4;">{feature}</span></div>'
                            )

                        ui.space()

                        def make_handler(t=tier["tier_key"]):
                            def handler():
                                selected_tier["value"] = t
                                if tier_select_ref["widget"]:
                                    tier_select_ref["widget"].value = t
                                ui.run_javascript(
                                    "document.getElementById('cadastro-mentoria').scrollIntoView({behavior:'smooth'})"
                                )
                            return handler

                        ui.button(
                            "Quero este plano",
                            on_click=make_handler(),
                        ).classes("w-full mt-2 bg-amber-600 text-white rounded-xl py-2 hover:bg-amber-700")

# CTA final — substitui o form inline. Tier já vem selecionado
        # pelo card clicado acima; default pro básico se ninguém clicou nada.
        with ui.column().classes("w-full items-center py-16 px-4"):
            ui.label("Pronto para começar?").classes("text-3xl font-bold text-stone-800 mb-2 text-center")
            ui.label(
                "O cadastro leva menos de 2 minutos."
            ).classes("text-stone-500 mb-8 text-center")

            def go_to_signup():
                tier = selected_tier["value"] or "mentoria_basico"
                ui.navigate.to(f"/mentoria/cadastro?tier={tier}")

            ui.button("Quero começar", on_click=go_to_signup).classes(
                "bg-amber-600 text-white rounded-xl px-10 py-3 text-lg hover:bg-amber-700"
            )

        # footer
        with ui.row().classes("w-full px-8 py-6 bg-stone-800 justify-center"):
            ui.label("© 2026 GoCanada — Todos os direitos reservados").classes("text-stone-400 text-sm")
