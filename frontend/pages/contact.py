# pages/contact.py
#
# Página de contato. NÃO tem formulário porque não existe endpoint de
# backend pra receber mensagem de contato (só existe create_lead, que é
# outra coisa — vira lead comercial, não mensagem livre). Um form que não
# manda nada pra lugar nenhum é pior que um mailto que funciona hoje.
#
# Se decidir que quer formulário de verdade depois, precisa de:
#   - tabela ContactMessage (ou reaproveitar Lead com um campo message)
#   - endpoint POST /contact no backend
#   - notificação por email pro contato@gocanadabr.com.br via Resend
# Isso NÃO foi construído.
#
# Paleta/fontes/header/footer vêm de pages/layout.py.

from nicegui import ui
from pages.layout import design_tokens, site_header, site_footer

CONTACT_EMAIL = "contato@gocanadabr.com.br"


def contact_page() -> None:
    design_tokens()

    with ui.column().classes("w-full min-h-screen bg-[#F5F0E6] font-body"):

        site_header("contato")

        with ui.column().classes("w-full items-center py-24 px-4 flex-grow"):
            with ui.column().classes("w-full max-w-lg gap-6 text-center items-center"):
                ui.label("Fale com a gente").classes(
                    "font-display text-4xl font-semibold text-[#16233D] mb-2"
                )
                ui.label(
                    "Dúvidas sobre relatório, mentoria ou qualquer outro assunto: "
                    "manda um email direto."
                ).classes("text-[#4B5563] text-lg")

                with ui.card().classes(
                    "w-full p-8 rounded-none shadow-md bg-white items-center gap-4"
                ):
                    ui.icon("mail").classes("text-4xl text-[#A6402F]")
                    ui.link(CONTACT_EMAIL, f"mailto:{CONTACT_EMAIL}").classes(
                        "font-mono text-xl text-[#A6402F] hover:text-[#8a3327]"
                    )
                    ui.label("Respondemos em até 2 dias úteis.").classes(
                        "text-[#4B5563]/60 text-sm font-mono"
                    )

        site_footer()
