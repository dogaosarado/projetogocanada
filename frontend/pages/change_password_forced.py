# pages/change_password_forced.py

from nicegui import ui
from state.user import get_token, is_logged_in, must_change_password, clear_must_change_password
from frontend.services.api import change_password
from pages.layout import design_tokens, brand_logo


def change_password_forced_page() -> None:
    design_tokens()
    if not is_logged_in():
        ui.navigate.to("/login")
        return
    if not must_change_password():
        ui.navigate.to("/painel")
        return

    token = get_token()

    with ui.column().classes("w-full min-h-screen bg-[#F5F0E6] font-body"):
        with ui.row().classes(
            "w-full px-8 py-5 bg-[#16233D] justify-start items-center"
        ):
            brand_logo()

        with ui.column().classes("w-full items-center justify-center flex-1 px-4 py-16"):
            with ui.card().classes(
                "w-96 p-8 shadow-md rounded-none bg-white border hairline"
            ):
                ui.label("Defina sua senha").classes(
                    "font-display text-2xl font-semibold text-[#A6402F] mb-1"
                )
                ui.label(
                    "Por segurança, troque a senha temporária recebida por email antes de continuar."
                ).classes("text-[#4B5563] mb-6 text-sm")

                current = ui.input("Senha temporária", password=True).classes("w-full")
                new = ui.input("Nova senha", password=True).classes("w-full mt-3")
                confirm = ui.input("Confirmar nova senha", password=True).classes("w-full mt-3")
                error_msg = ui.label("").classes("text-red-500 text-sm mt-2")
                error_msg.set_visibility(False)

                async def handle_submit():
                    if not current.value or not new.value:
                        error_msg.text = "Preencha todos os campos."
                        error_msg.set_visibility(True)
                        return
                    if new.value != confirm.value:
                        error_msg.text = "As senhas novas não coincidem."
                        error_msg.set_visibility(True)
                        return
                    ok, text = await change_password(token, current.value, new.value)
                    if ok:
                        clear_must_change_password()
                        ui.navigate.to("/painel")
                    else:
                        error_msg.text = text
                        error_msg.set_visibility(True)

                ui.button("Confirmar", on_click=handle_submit).classes(
                    "w-full mt-4 bg-[#A6402F] text-[#F5F0E6] rounded-none py-2 "
                    "font-mono text-sm tracking-wide hover:bg-[#8a3327]"
                )
