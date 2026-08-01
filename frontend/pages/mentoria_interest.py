# pages/mentoria_interest.py

from nicegui import ui
from pages.layout import brand_logo


def mentoria_interest_page() -> None:
    with ui.column().classes("w-full min-h-screen bg-stone-50"):
        with ui.row().classes("w-full px-8 py-5 bg-white shadow-sm justify-start items-center"):
            brand_logo()

        with ui.column().classes("w-full items-center justify-center flex-1 px-4 py-16"):
            with ui.card().classes("w-full max-w-lg p-10 shadow-lg rounded-2xl bg-white"):
                ui.icon("mail", size="4rem").classes("text-amber-600 mb-4 self-center")
                ui.label("Cadastro de mentoria recebido!").classes(
                    "text-2xl font-bold text-stone-800 mb-4 text-center"
                )

                steps = [
                    "Confira seu email — enviamos uma senha temporária de acesso.",
                    "Entre na plataforma com essa senha; você será obrigado a trocá-la no primeiro acesso.",
                    "Seu painel já estará com as universidades e programas que você escolheu no cadastro.",
                    "As instruções de pagamento chegam em um email de acompanhamento — a mentoria começa após a confirmação.",
                ]
                for i, step in enumerate(steps, start=1):
                    with ui.row().classes("w-full gap-3 items-start mb-3"):
                        ui.label(str(i)).classes(
                            "flex-shrink-0 w-6 h-6 rounded-full bg-amber-600 text-white text-sm "
                            "flex items-center justify-center font-bold"
                        )
                        ui.label(step).classes("text-stone-600")

                with ui.row().classes("w-full justify-center"):
                    ui.button(
                        "Entrar agora",
                        on_click=lambda: ui.navigate.to("/login")
                    ).classes("mt-6 bg-amber-600 text-white rounded-xl px-6 py-2 hover:bg-amber-700")