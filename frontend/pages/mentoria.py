# pages/mentoria.py
#
# Página dedicada à mentoria (produto independente do relatório).
# Conteúdo abaixo é placeholder — subtítulos, texto e bullets marcados com
# TODO são pra você reescrever com a proposta de valor real de cada etapa.

from nicegui import ui
from pages.layout import brand_logo
from services.api import create_lead
from pages.landing import MENTORSHIP_TIERS


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
                    "[São reuniões preparatórias para a candidatura. Com elas, você entende o processo seletivo de pós-graduação "
                    "no Canadá em detalhe — editais, prazos, critérios de avaliação, documentação exigida por universidade e "
                    "departamento. A mentoria desmistifica etapas que costumam travar o candidato (carta de motivação, currículo "
                    "acadêmico, contato com potenciais orientadores) e ajuda a organizar ideias e documentos de forma estruturada. "
                    "O objetivo é candidatura inteligente: decisões embasadas em cima do seu perfil real e seus objetivos acadêmicos.]"
                ).classes("text-stone-600 leading-relaxed")

        # subtítulo 2 — para quem é
        with ui.column().classes("w-full items-center py-16 px-4"):
            with ui.column().classes("max-w-3xl gap-4"):
                ui.label("Para quem é").classes("text-3xl font-bold text-stone-800 mb-2")
                ui.html(
                    "<ul style='color:#57534e; line-height:1.6; padding-left:1.2rem;'>"
                    "<li>[Para quem decidiu fazer uma pós no Canadá]</li>"
                    "<li>[Para quem quer realmente entender o processo seletivo]</li>"
                    "<li>[Para quem quer tomar as melhores decisões durante a aplicação]</li>"
                    "</ul>"
                )

        # subtítulo 3 — como funciona (etapas)
        with ui.column().classes("w-full items-center py-16 px-4 bg-white"):
            with ui.column().classes("max-w-3xl gap-4"):
                ui.label("Como funciona").classes("text-3xl font-bold text-stone-800 mb-2")
                ui.html(
                    "<ol style='color:#57534e; line-height:1.6; padding-left:1.2rem;'>"
                    "<li>[Os encontros são focados nos seguintes objetivos:]</li>"
                    "<li>[1- Apresentação da dinâmica de aplicação e alinhamento com a candidatura;]</li>"
                    "<li>[2- Preparação documental e textual;]</li>"
                    "<li>[3- Identificação de potenciais departamentos e supervisores;]</li>"
                    "<li>[4- Estratégias de contato e engajamento.]</li>"
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

        # formulário de interesse
        with ui.column().classes("w-full items-center py-16 px-4").props('id="cadastro-mentoria"'):
            ui.label("Comece agora").classes("text-3xl font-bold text-stone-800 mb-2 text-center")
            ui.label(
                "Preencha seus dados e entraremos em contato para agendar o primeiro encontro."
            ).classes("text-stone-500 mb-8 text-center")

            with ui.card().classes("w-full max-w-md p-8 shadow-lg rounded-2xl bg-white"):
                name_input = ui.input("Nome completo").classes("w-full")
                email_input = ui.input("Email").classes("w-full mt-3")

                tier_select = ui.select(
                    {
                        "mentoria_basico": "Básico — R$ 1.500 (8 encontros)",
                        "mentoria_intermediario": "Intermediário — R$ 2.000 (10 encontros)",
                        "mentoria_avancado": "Avançado — R$ 3.000 (12 encontros)",
                    },
                    label="Plano",
                    value="mentoria_basico",
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
                    # NOTA: create_lead() envia tier_val direto pro backend.
                    # Os valores "mentoria_*" só fazem sentido se o backend
                    # souber diferenciar lead de mentoria de lead de relatório.
                    # Ver aviso no final da resposta sobre isso.
                    result = create_lead(name_input.value, email_input.value, tier_val)
                    if result:
                        ui.navigate.to("/interesse")
                    else:
                        error_msg.text = "Erro ao cadastrar. Tente novamente."
                        error_msg.set_visibility(True)

                ui.button("Enviar", on_click=handle_interest).classes(
                    "w-full mt-6 bg-amber-600 text-white rounded-xl py-2 hover:bg-amber-700"
                )

        # footer
        with ui.row().classes("w-full px-8 py-6 bg-stone-800 justify-center"):
            ui.label("© 2026 GoCanada — Todos os direitos reservados").classes("text-stone-400 text-sm")
