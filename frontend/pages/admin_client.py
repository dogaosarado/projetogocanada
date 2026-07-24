# pages/admin_client.py

from nicegui import ui
import httpx
import os
from dotenv import load_dotenv
from state.user import get_token

load_dotenv()
API_URL = os.getenv("API_URL", "http://localhost:8000")


def get_client_detail(token: str, user_id: int) -> dict | None:
    try:
        response = httpx.get(
            f"{API_URL}/admin/users/{user_id}/detail",
            headers={"Authorization": f"bearer {token}"},
        )
        if response.status_code == 200:
            return response.json()
        return None
    except Exception:
        return None


def add_meeting(token: str, user_id: int, title: str, scheduled_at: str, notes: str) -> dict | None:
    try:
        response = httpx.post(
            f"{API_URL}/admin/users/{user_id}/meetings",
            json={"title": title, "scheduled_at": scheduled_at, "notes": notes or None},
            headers={"Authorization": f"bearer {token}"},
        )
        if response.status_code == 201:
            return response.json()
        return None
    except Exception:
        return None


def add_deadline(token: str, user_id: int, label: str, due_date: str) -> dict | None:
    try:
        response = httpx.post(
            f"{API_URL}/admin/users/{user_id}/deadlines",
            json={"label": label, "due_date": due_date},
            headers={"Authorization": f"bearer {token}"},
        )
        if response.status_code == 201:
            return response.json()
        return None
    except Exception:
        return None


def admin_client_page(user_id: int) -> None:
    token = get_token()
    detail = get_client_detail(token, user_id)

    with ui.column().classes("w-full min-h-screen bg-stone-50 items-center py-12 px-4"):
        with ui.card().classes("w-full max-w-2xl p-8 shadow-lg rounded-2xl bg-white"):
            ui.button("← Voltar", on_click=lambda: ui.navigate.to("/admin")).classes(
                "bg-stone-200 text-stone-700 rounded-xl px-4 py-2 mb-4"
            )

            if not detail:
                ui.label("Cliente não encontrado.").classes("text-red-500")
                return

            ui.label(detail["email"]).classes("text-2xl font-bold text-amber-700")
            status = "Ativo" if detail["is_active"] else "Inativo"
            ui.label(f"{detail['tier'].capitalize()} — {status}").classes("text-stone-500 mb-6")

            ui.separator().classes("my-4")

            # reuniões
            ui.label("Reuniões").classes("text-lg font-semibold text-stone-700 mb-2")
            for m in detail["meetings"]:
                with ui.row().classes("w-full justify-between py-1 border-b border-stone-100"):
                    ui.label(m["title"])
                    ui.label(m["scheduled_at"].replace("T", " ")[:16]).classes("text-stone-500 text-sm")
            if not detail["meetings"]:
                ui.label("Nenhuma reunião cadastrada.").classes("text-stone-400 text-sm")

            with ui.row().classes("w-full gap-2 items-end mt-3 flex-wrap"):
                m_title = ui.input("Título").classes("flex-1")
                m_date = ui.input("Data/hora").props('type=datetime-local').classes("flex-1")
                m_notes = ui.input("Notas (opcional)").classes("flex-1")
                m_msg = ui.label("").classes("text-sm")
                m_msg.set_visibility(False)

                def handle_add_meeting():
                    if not m_title.value or not m_date.value:
                        m_msg.text = "Preencha título e data."
                        m_msg.classes("text-red-500")
                        m_msg.set_visibility(True)
                        return
                    result = add_meeting(token, user_id, m_title.value, m_date.value, m_notes.value)
                    if result:
                        ui.navigate.to(f"/admin/users/{user_id}")
                    else:
                        m_msg.text = "Erro ao adicionar reunião."
                        m_msg.classes("text-red-500")
                        m_msg.set_visibility(True)

                ui.button("Adicionar", on_click=handle_add_meeting).classes(
                    "bg-amber-600 text-white rounded-xl px-4 py-2"
                )

            ui.separator().classes("my-4")

            # prazos
            ui.label("Prazos").classes("text-lg font-semibold text-stone-700 mb-2")
            for d in detail["deadlines"]:
                with ui.row().classes("w-full justify-between py-1 border-b border-stone-100"):
                    ui.label(d["label"])
                    ui.label(d["due_date"]).classes("text-stone-500 text-sm")
            if not detail["deadlines"]:
                ui.label("Nenhum prazo cadastrado.").classes("text-stone-400 text-sm")

            with ui.row().classes("w-full gap-2 items-end mt-3 flex-wrap"):
                d_label = ui.input("Descrição").classes("flex-1")
                d_date = ui.input("Data").props('type=date').classes("flex-1")
                d_msg = ui.label("").classes("text-sm")
                d_msg.set_visibility(False)

                def handle_add_deadline():
                    if not d_label.value or not d_date.value:
                        d_msg.text = "Preencha descrição e data."
                        d_msg.classes("text-red-500")
                        d_msg.set_visibility(True)
                        return
                    result = add_deadline(token, user_id, d_label.value, d_date.value)
                    if result:
                        ui.navigate.to(f"/admin/users/{user_id}")
                    else:
                        d_msg.text = "Erro ao adicionar prazo."
                        d_msg.classes("text-red-500")
                        d_msg.set_visibility(True)

                ui.button("Adicionar", on_click=handle_add_deadline).classes(
                    "bg-amber-600 text-white rounded-xl px-4 py-2"
                )