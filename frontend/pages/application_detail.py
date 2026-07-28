# pages/application_detail.py

from nicegui import ui
from state.user import get_token, is_logged_in
from services.api import get_application_detail, toggle_application_checklist_item
from pages.layout import authenticated_header


def application_detail_page(application_id: int) -> None:
    if not is_logged_in():
        ui.navigate.to("/login")
        return

    token = get_token()
    data = get_application_detail(token, application_id)

    with ui.column().classes("w-full min-h-screen bg-stone-50 items-center py-8 px-4"):
        authenticated_header()

        with ui.column().classes("w-full max-w-2xl gap-6 mt-4"):
            ui.button("← Voltar ao painel", on_click=lambda: ui.navigate.to("/painel")).classes(
                "bg-stone-200 text-stone-700 rounded-xl px-4 py-2 self-start"
            )

            if not data:
                with ui.card().classes("w-full p-8 text-center"):
                    ui.label("Candidatura não encontrada.").classes("text-red-500")
                return

            # cabeçalho da candidatura
            with ui.card().classes("w-full p-6 rounded-2xl shadow-sm bg-white"):
                if data.get("is_custom"):
                    ui.label("Personalizada").classes("text-xs text-amber-600 font-semibold uppercase mb-1")
                ui.label(data["university"]).classes("text-2xl font-bold text-stone-800")
                ui.label(data["department"]).classes("text-stone-500 mb-2")
                if data.get("url"):
                    ui.link("Ver página do programa", data["url"], new_tab=True).classes("text-amber-700 text-sm")

            # prazos
            with ui.card().classes("w-full p-6 rounded-2xl shadow-sm bg-white"):
                ui.label("Prazos desta candidatura").classes("text-lg font-bold text-stone-800 mb-3")
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
                        result = toggle_application_checklist_item(token, application_id, item_key)
                        if result is None:
                            checkbox.value = not e.value  # revert on failure
                            ui.notify("Erro ao atualizar item.", color="negative")
                    return handler

                for item in checklist:
                    with ui.row().classes("w-full items-center py-1"):
                        cb = ui.checkbox(item["label"], value=item["completed"])
                        cb.on_value_change(make_toggle_handler(item["key"], cb))
