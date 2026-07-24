# pages/dashboard.py

# pyrefly: ignore [missing-import]
from nicegui import ui
from state.user import get_token, is_logged_in, get_is_active
from services.api import get_dashboard, toggle_checklist_item
from pages.layout import authenticated_header


def dashboard_page() -> None:
    if not is_logged_in():
        ui.navigate.to("/login")
        return
    if not get_is_active():
        ui.navigate.to("/interesse")  # or wherever makes sense — "aguardando ativação" messaging
        return
    token = get_token()
    data = get_dashboard(token)

    with ui.column().classes("w-full min-h-screen bg-stone-50 items-center py-8 px-4"):
        authenticated_header()

        if not data:
            with ui.card().classes("w-full max-w-2xl p-8 mt-6 text-center"):
                ui.label("Erro ao carregar seu painel. Tente novamente mais tarde.").classes(
                    "text-red-500"
                )
            return

        with ui.column().classes("w-full max-w-2xl gap-6 mt-4"):

            # plano
            with ui.card().classes("w-full p-6 rounded-2xl shadow-sm bg-white"):
                ui.label(f"Plano {data['tier'].capitalize()}").classes(
                    "text-xl font-bold text-amber-700"
                )
                ui.button(
                    "Preencher formulário de universidades",
                    on_click=lambda: ui.navigate.to("/formulario"),
                ).classes("mt-3 bg-amber-600 text-white rounded-xl px-4 py-2 hover:bg-amber-700")

            # reuniões
            with ui.card().classes("w-full p-6 rounded-2xl shadow-sm bg-white"):
                ui.label("Reuniões com o consultor").classes("text-lg font-bold text-stone-800 mb-3")
                meetings = data.get("meetings", [])
                if not meetings:
                    ui.label("Nenhuma reunião agendada ainda.").classes("text-stone-400 text-sm")
                for m in meetings:
                    with ui.row().classes("w-full justify-between items-center py-2 border-b border-stone-100"):
                        with ui.column().classes("gap-0"):
                            ui.label(m["title"]).classes("text-stone-700 font-medium")
                            if m.get("notes"):
                                ui.label(m["notes"]).classes("text-stone-400 text-sm")
                        ui.label(m["scheduled_at"].replace("T", " ")[:16]).classes(
                            "text-amber-700 font-medium text-sm"
                        )

            # prazos
            with ui.card().classes("w-full p-6 rounded-2xl shadow-sm bg-white"):
                ui.label("Prazos de candidatura").classes("text-lg font-bold text-stone-800 mb-3")
                deadlines = data.get("deadlines", [])
                if not deadlines:
                    ui.label("Nenhum prazo cadastrado ainda.").classes("text-stone-400 text-sm")
                for d in deadlines:
                    with ui.row().classes("w-full justify-between items-center py-2 border-b border-stone-100"):
                        ui.label(d["label"]).classes("text-stone-700")
                        ui.label(d["due_date"]).classes("text-amber-700 font-medium text-sm")

            # checklist
            with ui.card().classes("w-full p-6 rounded-2xl shadow-sm bg-white"):
                ui.label("Checklist de documentos").classes("text-lg font-bold text-stone-800 mb-3")
                checklist = data.get("checklist", [])

                def make_toggle_handler(item_key, checkbox):
                    def handler(e):
                        result = toggle_checklist_item(token, item_key)
                        if result is None:
                            checkbox.value = not e.value  # revert on failure
                            ui.notify("Erro ao atualizar item.", color="negative")
                    return handler

                for item in checklist:
                    with ui.row().classes("w-full items-center py-1"):
                        cb = ui.checkbox(item["label"], value=item["completed"])
                        cb.on_value_change(make_toggle_handler(item["key"], cb))