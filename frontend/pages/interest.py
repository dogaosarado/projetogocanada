# pages/interest.py

from nicegui import ui
from pages.layout import brand_logo

def interest_page() -> None:
    with ui.column().classes("w-full min-h-screen bg-stone-50"):
        with ui.row().classes("w-full px-8 py-5 bg-white shadow-sm justify-start items-center"):
            brand_logo()

        with ui.column().classes("w-full items-center justify-center flex-1 px-4 py-16"):
            with ui.card().classes("w-full max-w-lg p-10 shadow-lg rounded-2xl bg-white text-center"):
                ui.icon("mail", size="4rem").classes("text-amber-600 mb-4")
                ui.label("Recebemos seu pedido!").classes("text-2xl font-bold text-stone-800 mb-2")
                ui.label(
                    "Seu relatório será enviado em até 48 horas após a confirmação do pagamento."
                ).classes("text-stone-500 mb-6")

                ui.button(
                    "Voltar ao início",
                    on_click=lambda: ui.navigate.to("/")
                ).classes("mt-2 bg-amber-600 text-white rounded-xl px-6 py-2 hover:bg-amber-700")