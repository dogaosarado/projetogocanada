# pages/about.py

from nicegui import ui


def about_page() -> None:
    with ui.column().classes("w-full min-h-screen bg-stone-50"):

        with ui.row().classes("w-full px-8 py-5 bg-white shadow-sm justify-between items-center"):
            ui.label("GoCanada").classes(
                "text-2xl font-bold text-amber-700 cursor-pointer"
            ).on("click", lambda: ui.navigate.to("/"))
            with ui.row().classes("gap-3 items-center"):
                ui.button("Blog", on_click=lambda: ui.navigate.to("/blog")).props("flat color=amber")
                ui.button("Entrar", on_click=lambda: ui.navigate.to("/login")).classes(
                    "bg-amber-600 text-white rounded-xl px-5 py-2 hover:bg-amber-700"
                )

        with ui.column().classes("w-full items-center py-20 px-4"):
            with ui.column().classes("w-full max-w-2xl gap-6"):
                ui.label("Quem somos").classes("text-4xl font-bold text-stone-800 mb-2")

                ui.label(
                    "A GoCanadaBR nasceu para ajudar estudantes brasileiros a planejar sua "
                    "pós-graduação no Canadá com informação de qualidade, no lugar de achismo "
                    "e planilha genérica de fórum."
                ).classes("text-stone-600 text-lg")

                ui.label(
                    "Fazemos o levantamento detalhado de universidades, programas, professores "
                    "e prazos, para que você possa investir seu tempo na candidatura em si — "
                    "não em garimpar informação espalhada em dezenas de sites em inglês."
                ).classes("text-stone-600 text-lg")

                ui.label(
                    "Trabalhamos com pesquisa individualizada por plano contratado: quanto mais "
                    "aprofundado o plano, mais universidades, professores e contexto de pesquisa "
                    "entregamos por candidatura."
                ).classes("text-stone-600 text-lg")

        with ui.column().classes("w-full items-center py-20 px-4"):
            with ui.column().classes("w-full max-w-2xl gap-6"):
                ui.label("Consultor").classes("text-4xl font-bold text-stone-800 mb-2")

                ui.label(
                    "Gustavo Denani é candidato de Ph.D em Antropologia pela Universidade de Ottawa."
                    "Morou em Ottawa e em Montreal durante 2021 e 2024, com experiência em processos"
                    "seletivos e editais de bolsa. "
                ).classes("text-stone-600 text-lg")

                ui.button(
                    "Ver planos", on_click=lambda: ui.navigate.to("/#planos")
                ).classes("bg-amber-600 text-white rounded-xl px-6 py-2 hover:bg-amber-700 w-fit mt-4")

        with ui.row().classes("w-full px-8 py-6 bg-stone-800 justify-center"):
            ui.label("© 2026 GoCanada — Todos os direitos reservados").classes(
                "text-stone-400 text-sm"
            )
