# pages/contact.py
#
# Página de contato. NÃO tem formulário porque não existe endpoint de
# backend pra receber mensagem de contato (só existe create_lead, que é
# outra coisa — vira lead comercial, não mensagem livre). Construir um
# formulário aqui empurraria pra você criar rota + tabela + email de
# notificação no backend antes de funcionar de verdade. Isso não é
# "não fazer o certo", é não fazer o errado rápido: um form fake que
# não envia nada é pior que um mailto que funciona hoje.
#
# Se decidir que quer formulário de verdade depois, precisa de:
#   - tabela ContactMessage (ou reaproveitar Lead com um campo message)
#   - endpoint POST /contact no backend
#   - notificação por email pro contato@gocanadabr.com.br via Resend
# Isso NÃO foi construído. O que está aqui é o que dá pra entregar
# fechado com o que já existe.

from nicegui import ui
from pages.layout import brand_logo

CONTACT_EMAIL = "contato@gocanadabr.com.br"


def contact_page() -> None:
    with ui.column().classes("w-full min-h-screen bg-stone-50"):

        with ui.row().classes("w-full px-8 py-5 bg-white shadow-sm justify-between items-center"):
            brand_logo()
            with ui.row().classes("gap-3 items-center"):
                ui.button("Mentoria", on_click=lambda: ui.navigate.to("/")).props(
                    "flat color=amber"
                )
                ui.button("Relatórios", on_click=lambda: ui.navigate.to("/relatorio")).props(
                    "flat color=amber"
                )
                ui.button("Quem somos", on_click=lambda: ui.navigate.to("/quem-somos")).props(
                    "flat color=amber"
                )
                ui.button("Entrar", on_click=lambda: ui.navigate.to("/login")).classes(
                    "bg-amber-600 text-white rounded-xl px-5 py-2 hover:bg-amber-700"
                )

        with ui.column().classes("w-full items-center py-24 px-4 flex-grow"):
            with ui.column().classes("w-full max-w-lg gap-6 text-center items-center"):
                ui.label("Fale com a gente").classes("text-4xl font-bold text-stone-800 mb-2")
                ui.label(
                    "Dúvidas sobre relatório, mentoria ou qualquer outro assunto: "
                    "manda um email direto."
                ).classes("text-stone-600 text-lg")

                with ui.card().classes("w-full p-8 rounded-2xl shadow-md bg-white items-center gap-4"):
                    ui.icon("mail").classes("text-4xl text-amber-600")
                    ui.link(CONTACT_EMAIL, f"mailto:{CONTACT_EMAIL}").classes(
                        "text-xl font-semibold text-amber-700 hover:text-amber-800"
                    )
                    ui.label(
                        "Respondemos em até 2 dias úteis."
                    ).classes("text-stone-400 text-sm")

        with ui.row().classes("w-full px-8 py-6 bg-stone-800 justify-center"):
            ui.label("© 2026 GoCanada — Todos os direitos reservados").classes(
                "text-stone-400 text-sm"
            )
