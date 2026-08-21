# pages/login.py

from nicegui import ui, app
from frontend.services.api import login, get_me
from state.user import set_user
from pages.layout import design_tokens, brand_logo


def login_page() -> None:
    design_tokens()
    with ui.column().classes("w-full min-h-screen bg-[#F5F0E6] font-body"):
        with ui.row().classes(
            "w-full px-8 py-5 bg-[#16233D] justify-start items-center"
        ):
            brand_logo()

        with ui.column().classes("w-full items-center justify-center flex-1 px-4 py-16"):
            with ui.card().classes(
                "w-96 p-8 shadow-md rounded-none bg-white border hairline"
            ):
                ui.label("GoCanadaBR").classes(
                    "font-display text-3xl font-semibold text-[#A6402F] mb-1"
                )
                ui.label("Acesse sua conta").classes(
                    "text-[#4B5563] mb-6 font-mono text-sm"
                )

                email = ui.input("Email").classes("w-full")
                password = ui.input("Senha", password=True, password_toggle_button=True).classes("w-full mt-2")
                error_msg = ui.label("").classes("text-red-500 text-sm mt-1")
                error_msg.set_visibility(False)

                async def handle_login():
                    result, error = await login(email.value, password.value)
                    if result:
                        token = result["access_token"]
                        user, user_error = await get_me(token)
                        if user:
                            set_user(
                                token=token,
                                email=user["email"],
                                tier=user["tier"],
                                name=user.get("name"),
                                is_active=user.get("is_active", False),
                                is_admin=user.get("is_admin", False),
                                must_change_password=user.get("must_change_password", False),
                            )
                            if user.get("must_change_password"):
                                ui.navigate.to("/trocar-senha")
                            else:
                                ui.navigate.to("/painel")
                        else:
                            error_msg.text = user_error or "Erro ao buscar dados do usuário."
                            error_msg.set_visibility(True)
                    else:
                        error_msg.text = error or "Email ou senha incorretos."
                        error_msg.set_visibility(True)

                ui.button("Entrar", on_click=handle_login).classes(
                    "w-full mt-4 bg-[#A6402F] text-[#F5F0E6] rounded-none py-2 "
                    "font-mono text-sm tracking-wide hover:bg-[#8a3327]"
                )
