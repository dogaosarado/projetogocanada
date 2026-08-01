# pages/mentoria_interest.py

from nicegui import ui
from pages.layout import design_tokens, brand_logo


def mentoria_interest_page() -> None:
    design_tokens()
    with ui.column().classes("w-full min-h-screen bg-[#F5F0E6] font-body"):
        with ui.row().classes(
            "w-full px-8 py-5 bg-[#16233D] justify-start items-center"
        ):
            brand_logo()

        with ui.column().classes("w-full items-center justify-center flex-1 px-4 py-16"):
            with ui.card().classes(
                "w-full max-w-lg p-10 shadow-md rounded-none bg-white border hairline"
            ):
                ui.icon("mail", size="4rem").classes("text-[#A6402F] mb-4 self-center")
                ui.label("Cadastro de mentoria recebido!").classes(
                    "font-display text-2xl font-semibold text-[#16233D] mb-4 text-center"
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
                            "flex-shrink-0 w-6 h-6 rounded-full bg-[#A6402F] text-[#F5F0E6] "
                            "text-sm flex items-center justify-center font-mono font-medium"
                        )
                        ui.label(step).classes("text-[#4B5563]")

                with ui.row().classes("w-full justify-center"):
                    ui.button(
                        "Entrar agora",
                        on_click=lambda: ui.navigate.to("/login")
                    ).classes(
                        "mt-6 bg-[#A6402F] text-[#F5F0E6] rounded-none px-6 py-2 "
                        "font-mono text-xs tracking-wide hover:bg-[#8a3327]"
                    )
