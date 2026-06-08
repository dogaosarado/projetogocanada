# pages/landing.py

from nicegui import ui


TIERS = [
    {
        "name": "Básico",
        "price": "R$ 250",
        "universities": 2,
        "departments": 1,
        "professors": None,
        "features": [
            "2 universidades",
            "1 departamento por universidade",
            "Prazos do processo seletivo",
            "Proficiência em inglês exigida",
            "Tuition e valor da bolsa",
        ],
    },
    {
        "name": "Intermediário",
        "price": "R$ 400",
        "universities": 3,
        "departments": 1,
        "professors": 1,
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
        "universities": 4,
        "departments": 1,
        "professors": 2,
        "features": [
            "4 universidades",
            "1 departamento por universidade",
            "Tudo do plano Intermediário",
            "Ficha de 2 professores por departamento",
            "Desconto em consultoria personalizada",
        ],
    },
]


def landing_page() -> None:
    with ui.column().classes("w-full min-h-screen bg-stone-50"):

        # header
        with ui.row().classes("w-full px-8 py-5 bg-white shadow-sm justify-between items-center"):
            ui.label("GoCanada").classes("text-2xl font-bold text-amber-700")
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
            ui.button("Ver planos", on_click=lambda: ui.run_javascript("document.getElementById('planos').scrollIntoView({behavior:'smooth'})")).classes(
                "bg-amber-600 text-white rounded-xl px-8 py-3 text-lg hover:bg-amber-700"
            )

        # tiers
        with ui.column().classes("w-full items-center py-16 px-4 bg-white").props('id="planos"'):
            ui.label("Escolha seu plano").classes("text-3xl font-bold text-stone-800 mb-2 text-center")
            ui.label("Após o pagamento via Pix, você receberá acesso ao formulário.").classes(
                "text-stone-500 mb-10 text-center"
            )

            with ui.row().classes("gap-6 flex-wrap justify-center"):
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

                        ui.button(
                            "Quero este plano",
                            on_click=lambda: ui.navigate.to("/login"),
                        ).classes("w-full mt-2 bg-amber-600 text-white rounded-xl py-2 hover:bg-amber-700")

        # novidades
        with ui.column().classes("w-full items-center py-16 px-4"):
            ui.label("Novidades").classes("text-3xl font-bold text-stone-800 mb-8 text-center")
            with ui.row().classes("gap-6 flex-wrap justify-center max-w-4xl"):
                novidades = [
                    {
                        "titulo": "Como escolher seu orientador no Canadá",
                        "desc": "Entenda o papel do supervisor na pós-graduação canadense e como identificar o perfil certo para sua pesquisa.",
                        "data": "Jun 2026",
                    },
                    {
                        "titulo": "Prazos de candidatura 2025-2026",
                        "desc": "Um guia atualizado com os principais deadlines das universidades canadenses para o próximo ciclo.",
                        "data": "Mai 2026",
                    },
                    {
                        "titulo": "Bolsas disponíveis para brasileiros",
                        "desc": "Conheça as principais fontes de financiamento para estudantes brasileiros no Canadá.",
                        "data": "Abr 2026",
                    },
                ]
                for n in novidades:
                    with ui.card().classes("w-72 p-6 rounded-2xl shadow-sm bg-white"):
                        ui.label(n["data"]).classes("text-xs text-amber-600 font-medium mb-1")
                        ui.label(n["titulo"]).classes("text-stone-800 font-semibold mb-2")
                        ui.label(n["desc"]).classes("text-stone-500 text-sm")

        # footer
        with ui.row().classes("w-full px-8 py-6 bg-stone-800 justify-center"):
            ui.label("© 2026 GoCanada — Todos os direitos reservados").classes("text-stone-400 text-sm")