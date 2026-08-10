# pages/relatorio_interest.py

from nicegui import ui
from pages.layout import design_tokens, brand_logo


def relatorio_interest_page() -> None:
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
                ui.label("Pedido de relatório recebido!").classes(
                    "font-display text-2xl font-semibold text-[#16233D] mb-4 text-center"
                )
                ui.label(
                    "Confira seu email de confirmação. Em breve você recebe o link para "
                    "pagamento via Pix — assim que o pagamento for confirmado, seu "
                    "relatório é enviado por email em até 48 horas."
                ).classes("text-[#4B5563] text-center")

                with ui.row().classes("w-full justify-center"):
                    ui.button(
                        "Voltar para o site",
                        on_click=lambda: ui.navigate.to("/")
                    ).classes(
                        "mt-6 bg-[#A6402F] text-[#F5F0E6] rounded-none px-6 py-2 "
                        "font-mono text-xs tracking-wide hover:bg-[#8a3327]"
                    )
