# pages/interest.py

from nicegui import ui


def interest_page() -> None:
    with ui.column().classes("w-full min-h-screen bg-stone-50 items-center justify-center px-4"):
        with ui.card().classes("w-full max-w-lg p-10 shadow-lg rounded-2xl bg-white text-center"):
            ui.icon("mail", size="4rem").classes("text-amber-600 mb-4")
            ui.label("Cadastro recebido!").classes("text-2xl font-bold text-stone-800 mb-2")
            ui.label(
                "Enviamos suas credenciais de acesso por email. Você já pode entrar na "
                "plataforma, conhecer o painel e preencher o formulário com as universidades "
                "e programas do seu interesse."
            ).classes("text-stone-500 mb-6")

            ui.label(
                "O relatório é entregue após a confirmação do pagamento do plano escolhido "
                "— as instruções de pagamento chegam em um email de acompanhamento."
            ).classes("text-stone-400 text-sm")

            ui.button(
                "Entrar agora",
                on_click=lambda: ui.navigate.to("/login")
            ).classes("mt-6 bg-amber-600 text-white rounded-xl px-6 py-2 hover:bg-amber-700")
