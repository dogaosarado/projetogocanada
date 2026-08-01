# pages/confirmation.py

from nicegui import ui
from state.user import get_email, get_tier
from pages.layout import design_tokens, authenticated_header


def confirmation_page() -> None:
    design_tokens()
    with ui.column().classes(
        "w-full min-h-screen bg-[#F5F0E6] font-body items-center justify-center px-4"
    ):
        authenticated_header()
        with ui.card().classes(
            "w-full max-w-lg p-10 shadow-md rounded-none bg-white border hairline text-center"
        ):
            ui.icon("check_circle", size="4rem").classes("text-[#A6402F] mb-4")
            ui.label("Formulário enviado!").classes(
                "font-display text-2xl font-semibold text-[#16233D] mb-2"
            )
            ui.label(
                "Recebemos suas universidades e programas de interesse."
            ).classes("text-[#4B5563] mb-4")

            with ui.card().classes("w-full p-4 bg-[#F5F0E6] rounded-none border hairline mb-4"):
                ui.label(
                    "O relatório é entregue após a confirmação do pagamento do plano "
                    "escolhido. Você vai receber as instruções de pagamento em um email "
                    "de acompanhamento."
                ).classes("text-[#4B5563] text-sm")

            email = get_email()
            tier = get_tier()

            if email:
                ui.label(f"Email: {email}").classes("text-[#4B5563] text-sm font-mono")
            if tier:
                ui.label(f"Plano: {tier.capitalize()}").classes(
                    "text-[#4B5563] text-sm font-mono mb-6"
                )

            ui.button("Voltar ao painel", on_click=lambda: ui.navigate.to("/painel")).classes(
                "mt-4 bg-white border border-[#16233D]/20 text-[#16233D] rounded-none "
                "px-6 py-2 font-mono text-xs tracking-wide hover:bg-[#F5F0E6]"
            )
