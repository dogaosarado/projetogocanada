# pages/confirmation.py

from nicegui import ui
from state.user import get_email, get_tier
from pages.layout import authenticated_header


def confirmation_page() -> None:
    with ui.column().classes("w-full min-h-screen bg-stone-50 items-center justify-center px-4"):
        authenticated_header()
        with ui.card().classes("w-full max-w-lg p-10 shadow-lg rounded-2xl bg-white text-center"):
            ui.icon("check_circle", size="4rem").classes("text-amber-600 mb-4")
            ui.button("Voltar ao painel", on_click=lambda: ui.navigate.to("/painel")).classes(
    "mt-4 bg-stone-200 text-stone-700 rounded-xl px-6 py-2 hover:bg-stone-300"
)
            ui.label("Pedido enviado!").classes("text-2xl font-bold text-stone-800 mb-2")
            ui.label(
                "Recebemos sua solicitação. O consultor irá pesquisar os professores "
                "e entrar em contato com você em breve."
            ).classes("text-stone-500 mb-6")

            email = get_email()
            tier = get_tier()

            if email:
                ui.label(f"Email: {email}").classes("text-stone-600 text-sm")
            if tier:
                ui.label(f"Plano: {tier.capitalize()}").classes("text-stone-600 text-sm mb-6")