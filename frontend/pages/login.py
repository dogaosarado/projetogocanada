# pages/login.py

from nicegui import ui, app
from services.api import login, get_me
from state.user import set_user


def login_page() -> None:
    with ui.column().classes("w-full min-h-screen items-center justify-center bg-stone-50"):
        with ui.card().classes("w-96 p-8 shadow-lg rounded-2xl bg-white"):
            ui.label("GoCanada").classes("text-3xl font-bold text-amber-700 mb-1")
            ui.label("Acesse sua conta").classes("text-stone-500 mb-6")

            email = ui.input("Email").classes("w-full")
            password = ui.input("Senha", password=True, password_toggle_button=True).classes("w-full mt-2")
            error_msg = ui.label("").classes("text-red-500 text-sm mt-1")
            error_msg.set_visibility(False)

            def handle_login():
                result = login(email.value, password.value)
                if result:
                    token = result["access_token"]
                    user = get_me(token)
                    print(f"USER FROM API: {user}")
                    if user:
                        set_user(token=token, email=user["email"], tier=user["tier"])
                        print(f"STORAGE AFTER SET: {app.storage.user}")
                        ui.navigate.to("/formulario")
                    else:
                        error_msg.text = "Erro ao buscar dados do usuário."
                        error_msg.set_visibility(True)
                else:
                    error_msg.text = "Email ou senha incorretos."
                    error_msg.set_visibility(True)

            ui.button("Entrar", on_click=handle_login).classes(
                "w-full mt-4 bg-amber-600 text-white rounded-xl py-2 hover:bg-amber-700"
            )