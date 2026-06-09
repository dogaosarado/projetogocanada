# pages/admin.py

from nicegui import ui
from state.user import get_token, get_tier, is_logged_in
from services.api import get_me
import httpx
import os
from dotenv import load_dotenv
from services.api import delete_user

load_dotenv()
API_URL = os.getenv("API_URL", "http://localhost:8000")


def get_users(token: str) -> list:
    try:
        response = httpx.get(
            f"{API_URL}/admin/users",
            headers={"Authorization": f"bearer {token}"},
        )
        if response.status_code == 200:
            return response.json()
        return []
    except Exception:
        return []


def create_user(token: str, email: str, password: str, tier: str) -> dict | None:
    try:
        response = httpx.post(
            f"{API_URL}/admin/users",
            json={"email": email, "password": password, "tier": tier},
            headers={"Authorization": f"bearer {token}"},
        )
        if response.status_code == 201:
            return response.json()
        return None
    except Exception:
        return None


def activate_user(token: str, user_id: int, tier: str) -> dict | None:
    try:
        response = httpx.patch(
            f"{API_URL}/admin/users/{user_id}/tier",
            json={"tier": tier},
            headers={"Authorization": f"bearer {token}"},
        )
        if response.status_code == 200:
            return response.json()
        return None
    except Exception:
        return None

def admin_page() -> None:
    if not is_logged_in():
        ui.navigate.to("/login")
        return

    token = get_token()
    tier = get_tier()

    if tier != "avancado":
        ui.navigate.to("/")
        return

    users = get_users(token)

    with ui.column().classes("w-full min-h-screen bg-stone-50 items-center py-12 px-4"):
        with ui.card().classes("w-full max-w-4xl p-8 shadow-lg rounded-2xl bg-white"):
            with ui.row().classes("w-full justify-between items-center mb-6"):
                ui.label("Painel Admin").classes("text-2xl font-bold text-amber-700")
                ui.button("Voltar", on_click=lambda: ui.navigate.to("/")).classes(
                    "bg-stone-200 text-stone-700 rounded-xl px-4 py-2"
                )

            # criar usuário
            ui.label("Novo cliente").classes("text-lg font-semibold text-stone-700 mb-2")
            with ui.row().classes("w-full gap-3 items-end flex-wrap"):
                new_email = ui.input("Email").classes("flex-1")
                new_password = ui.input("Senha", password=True).classes("flex-1")
                new_tier = ui.select(
                    {"basico": "Básico", "intermediario": "Intermediário", "avancado": "Avançado"},
                    label="Plano",
                    value="basico",
                ).classes("w-40")
                create_msg = ui.label("").classes("text-sm")
                create_msg.set_visibility(False)

                def handle_create():
                    result = create_user(token, new_email.value, new_password.value, new_tier.value)
                    if result:
                        create_msg.text = f"Usuário {result['email']} criado."
                        create_msg.classes("text-green-600")
                        create_msg.set_visibility(True)
                        new_email.value = ""
                        new_password.value = ""
                        ui.navigate.to("/admin")
                    else:
                        create_msg.text = "Erro ao criar usuário."
                        create_msg.classes("text-red-500")
                        create_msg.set_visibility(True)

                ui.button("Criar", on_click=handle_create).classes(
                    "bg-amber-600 text-white rounded-xl px-5 py-2 hover:bg-amber-700"
                )

            ui.separator().classes("my-6")

            # lista de usuários
            ui.label("Clientes").classes("text-lg font-semibold text-stone-700 mb-4")

            if not users:
                ui.label("Nenhum cliente cadastrado.").classes("text-stone-400")
            else:
                with ui.column().classes("w-full gap-3"):
                    for user in users:
                        with ui.card().classes("w-full p-4 bg-stone-50 rounded-xl"):
                            with ui.row().classes("w-full justify-between items-center flex-wrap gap-3"):
                                with ui.column().classes("gap-1"):
                                    ui.label(user["email"]).classes("font-medium text-stone-800")
                                    status = "Ativo" if user["is_active"] else "Inativo"
                                    status_color = "text-green-600" if user["is_active"] else "text-red-500"
                                    ui.label(f"{user['tier'].capitalize()} — {status}").classes(
                                        f"text-sm {status_color}"
                                    )

                                with ui.row().classes("gap-2 items-center"):
                                    tier_select = ui.select(
                                        {"basico": "Básico", "intermediario": "Intermediário", "avancado": "Avançado"},
                                        value=user["tier"],
                                    ).classes("w-36")
                                    activate_msg = ui.label("").classes("text-sm text-green-600")
                                    activate_msg.set_visibility(False)

                                    def handle_activate(uid=user["id"], ts=tier_select, msg=activate_msg):
                                        result = activate_user(token, uid, ts.value)
                                        if result:
                                            msg.text = "Ativado."
                                            msg.set_visibility(True)
                                        else:
                                            msg.text = "Erro."
                                            msg.set_visibility(True)
                                    def handle_delete(uid=user["id"]):
                                        result = delete_user(token, uid)
                                        if result:
                                            ui.navigate.to("/admin")
                                        else:
                                            ui.notify("Erro ao deletar.", color="negative")

                                    ui.button("Deletar", on_click=handle_delete).classes(
                                        "bg-red-500 text-white rounded-xl px-4 py-2 hover:bg-red-600"
                                    )
                                    ui.button("Ativar", on_click=handle_activate).classes(
                                        "bg-amber-600 text-white rounded-xl px-4 py-2 hover:bg-amber-700"
                                    )