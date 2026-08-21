# pages/admin_client.py

from nicegui import ui
import httpx
import os
from dotenv import load_dotenv
from state.user import get_token
from frontend.services.api import add_deadline_to_application, get_application_admin_detail
from pages.layout import authenticated_header

load_dotenv()
API_URL = os.getenv("API_URL", "http://localhost:8000")
_DEFAULT_TIMEOUT = 15


async def get_client_detail(token: str, user_id: int) -> dict | None:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{API_URL}/admin/users/{user_id}/detail",
                headers={"Authorization": f"bearer {token}"},
                timeout=_DEFAULT_TIMEOUT,
            )
        if response.status_code == 200:
            return response.json()
        return None
    except Exception:
        return None


async def add_meeting(token: str, user_id: int, title: str, scheduled_at: str, notes: str) -> dict | None:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{API_URL}/admin/users/{user_id}/meetings",
                json={"title": title, "scheduled_at": scheduled_at, "notes": notes or None},
                headers={"Authorization": f"bearer {token}"},
                timeout=_DEFAULT_TIMEOUT,
            )
        if response.status_code == 201:
            return response.json()
        return None
    except Exception:
        return None


def admin_client_page(user_id: int) -> None:
    token = get_token()

    with ui.column().classes("w-full min-h-screen bg-stone-50 items-center py-12 px-4"):
        authenticated_header()
        with ui.card().classes("w-full max-w-2xl p-8 shadow-lg rounded-2xl bg-white"):
            ui.button("← Voltar", on_click=lambda: ui.navigate.to("/admin")).classes(
                "bg-stone-200 text-stone-700 rounded-xl px-4 py-2 mb-4"
            )

            content = ui.column().classes("w-full")

        async def load():
            detail = await get_client_detail(token, user_id)

            with content:
                if not detail:
                    ui.label("Cliente não encontrado.").classes("text-red-500")
                    return

                ui.label(detail["email"]).classes("text-2xl font-bold text-amber-700")
                status = "Pago" if detail["is_active"] else "Pendente"
                ui.label(f"{detail['tier'].capitalize()} — {status}").classes("text-stone-500 mb-6")

                ui.separator().classes("my-4")

                # reuniões (gerais, não vinculadas a uma universidade)
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

                    async def handle_add_meeting():
                        if not m_title.value or not m_date.value:
                            m_msg.text = "Preencha título e data."
                            m_msg.classes("text-red-500")
                            m_msg.set_visibility(True)
                            return
                        result = await add_meeting(token, user_id, m_title.value, m_date.value, m_notes.value)
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

                # candidaturas — prazos agora são por universidade, não por cliente
                ui.label("Candidaturas e prazos").classes("text-lg font-semibold text-stone-700 mb-2")
                applications = detail.get("applications", [])

                if not applications:
                    ui.label(
                        "Cliente ainda não preencheu o formulário de universidades."
                    ).classes("text-stone-400 text-sm")

                for a in applications:
                    with ui.card().classes("w-full p-4 bg-stone-50 rounded-xl mb-3"):
                        ui.label(f"{a['university']} — {a['department']}").classes(
                            "font-medium text-stone-800"
                        )

                        app_detail = await get_application_admin_detail(token, a["id"])
                        existing_deadlines = app_detail.get("deadlines", []) if app_detail else []

                        if existing_deadlines:
                            with ui.column().classes("w-full gap-1 mt-2"):
                                for d in existing_deadlines:
                                    with ui.row().classes("w-full justify-between py-1 border-b border-stone-100"):
                                        ui.label(d["label"]).classes("text-stone-700 text-sm")
                                        ui.label(d["due_date"]).classes("text-stone-500 text-sm")
                        else:
                            ui.label("Nenhum prazo cadastrado ainda.").classes("text-stone-400 text-sm mt-2")

                        with ui.row().classes("w-full gap-2 items-end mt-2 flex-wrap"):
                            d_label = ui.input("Descrição do prazo").classes("flex-1")
                            d_date = ui.input("Data").props('type=date').classes("flex-1")
                            d_msg = ui.label("").classes("text-sm")
                            d_msg.set_visibility(False)

                            async def handle_add_deadline(app_id=a["id"], label=d_label, date=d_date, msg=d_msg):
                                if not label.value or not date.value:
                                    msg.text = "Preencha descrição e data."
                                    msg.classes("text-red-500")
                                    msg.set_visibility(True)
                                    return
                                result = await add_deadline_to_application(token, app_id, label.value, date.value)
                                if result:
                                    ui.navigate.to(f"/admin/users/{user_id}")
                                else:
                                    msg.text = "Erro ao adicionar prazo."
                                    msg.classes("text-red-500")
                                    msg.set_visibility(True)

                            ui.button("Adicionar prazo", on_click=handle_add_deadline).classes(
                                "bg-amber-600 text-white rounded-xl px-4 py-2"
                            )

        ui.timer(0, load, once=True)
