# pages/admin_relatorio.py
#
# Ferramenta manual pro fluxo de relatório: como nada é salvo em banco, não
# existe uma lista de "leads" pra clicar. O admin lê o email de notificação
# (nome/email/plano/links de departamento) e digita aqui na hora de mandar
# o link de pagamento, e de novo depois de conferir o Pix na conta.

from nicegui import ui
from pages.layout import design_tokens, brand_logo
from state.user import get_token
from frontend.services.api import send_relatorio_payment_link, confirm_relatorio_payment

TIER_OPTIONS = {
    "relatorio_gratis": "Grátis — R$ 0",
    "relatorio_basico": "Básico — R$ 150",
    "relatorio_intermediario": "Intermediário — R$ 250",
    "relatorio_avancado": "Avançado — R$ 400",
}


def admin_relatorio_page() -> None:
    design_tokens()
    token = get_token()

    with ui.column().classes("w-full min-h-screen bg-[#F5F0E6] font-body"):
        with ui.row().classes("w-full px-8 py-5 bg-[#16233D] justify-start items-center"):
            brand_logo()

        with ui.column().classes("w-full items-center py-12 px-4 gap-8"):

            # -----------------------------------------------------------------
            # Etapa 1: enviar link de pagamento
            # -----------------------------------------------------------------
            with ui.card().classes("w-full max-w-lg p-8 rounded-none bg-white border hairline"):
                ui.label("Enviar link de pagamento").classes(
                    "font-display text-xl font-semibold text-[#16233D] mb-1"
                )
                ui.label(
                    "Depois de ler o email de notificação do pedido."
                ).classes("text-[#4B5563] text-sm mb-4 font-mono")

                pl_name = ui.input("Nome do cliente").classes("w-full")
                pl_email = ui.input("Email do cliente").classes("w-full mt-3")
                pl_tier = ui.select(options=TIER_OPTIONS, label="Plano").classes("w-full mt-3")
                pl_pix = ui.input("Link do Pix").classes("w-full mt-3")

                pl_msg = ui.label("").classes("text-sm mt-3")
                pl_msg.set_visibility(False)

                def handle_send_payment_link():
                    if not (pl_name.value and pl_email.value and pl_tier.value and pl_pix.value):
                        pl_msg.text = "Preencha todos os campos."
                        pl_msg.classes(replace="text-red-500 text-sm mt-3")
                        pl_msg.set_visibility(True)
                        return
                    ok, error = send_relatorio_payment_link(
                        token, pl_name.value, pl_email.value, pl_tier.value, pl_pix.value
                    )
                    if ok:
                        pl_msg.text = "Link de pagamento enviado."
                        pl_msg.classes(replace="text-green-600 text-sm mt-3")
                    else:
                        pl_msg.text = error or "Erro ao enviar."
                        pl_msg.classes(replace="text-red-500 text-sm mt-3")
                    pl_msg.set_visibility(True)

                ui.button("Enviar link de pagamento", on_click=handle_send_payment_link).classes(
                    "w-full mt-6 bg-[#16233D] text-[#F5F0E6] rounded-none py-2 "
                    "font-mono text-xs tracking-wide hover:bg-[#0f182b]"
                )

            # -----------------------------------------------------------------
            # Etapa 2: confirmar pagamento recebido
            # -----------------------------------------------------------------
            with ui.card().classes("w-full max-w-lg p-8 rounded-none bg-white border hairline"):
                ui.label("Confirmar pagamento recebido").classes(
                    "font-display text-xl font-semibold text-[#16233D] mb-1"
                )
                ui.label(
                    "Depois de conferir o Pix na conta. Avisa o cliente que o "
                    "relatório chega em até 48h."
                ).classes("text-[#4B5563] text-sm mb-4 font-mono")

                cf_name = ui.input("Nome do cliente").classes("w-full")
                cf_email = ui.input("Email do cliente").classes("w-full mt-3")

                cf_msg = ui.label("").classes("text-sm mt-3")
                cf_msg.set_visibility(False)

                def handle_confirm_payment():
                    if not (cf_name.value and cf_email.value):
                        cf_msg.text = "Preencha nome e email."
                        cf_msg.classes(replace="text-red-500 text-sm mt-3")
                        cf_msg.set_visibility(True)
                        return
                    ok, error = confirm_relatorio_payment(token, cf_name.value, cf_email.value)
                    if ok:
                        cf_msg.text = "Confirmação enviada — cliente avisado do prazo de 48h."
                        cf_msg.classes(replace="text-green-600 text-sm mt-3")
                    else:
                        cf_msg.text = error or "Erro ao enviar."
                        cf_msg.classes(replace="text-red-500 text-sm mt-3")
                    cf_msg.set_visibility(True)

                ui.button("Confirmar pagamento", on_click=handle_confirm_payment).classes(
                    "w-full mt-6 bg-[#A6402F] text-[#F5F0E6] rounded-none py-2 "
                    "font-mono text-xs tracking-wide hover:bg-[#8a3327]"
                )
