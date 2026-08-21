# pages/application_detail.py

from nicegui import ui
from state.user import get_token, is_logged_in
from frontend.services.api import get_application_detail, toggle_application_checklist_item
from pages.layout import design_tokens, authenticated_header


def application_detail_page(application_id: int) -> None:
    design_tokens()
    if not is_logged_in():
        ui.navigate.to("/login")
        return

    token = get_token()

    with ui.column().classes(
        "w-full min-h-screen bg-[#F5F0E6] font-body items-center py-8 px-4"
    ):
        authenticated_header()

        with ui.column().classes("w-full max-w-2xl gap-6 mt-4"):
            ui.button("← Voltar ao painel", on_click=lambda: ui.navigate.to("/painel")).classes(
                "bg-white border border-[#16233D]/20 text-[#16233D] rounded-none px-4 py-2 "
                "font-mono text-xs tracking-wide hover:bg-[#F5F0E6] self-start"
            )

            content = ui.column().classes("w-full gap-6")

        async def load():
            data = await get_application_detail(token, application_id)

            with content:
                if not data:
                    with ui.card().classes("w-full p-8 rounded-none border hairline text-center"):
                        ui.label("Candidatura não encontrada.").classes("text-red-500")
                    return

                # cabeçalho da candidatura
                with ui.card().classes("w-full p-6 rounded-none shadow-sm bg-white border hairline"):
                    if data.get("is_custom"):
                        ui.label("Personalizada").classes(
                            "font-mono text-[10px] text-[#A6402F] tracking-widest uppercase mb-1"
                        )
                    ui.label(data["university"]).classes(
                        "font-display text-2xl font-semibold text-[#16233D]"
                    )
                    ui.label(data["department"]).classes("text-[#4B5563] mb-2")
                    if data.get("url"):
                        ui.link("Ver página do programa", data["url"], new_tab=True).classes(
                            "font-mono text-[#A6402F] text-sm"
                        )

                # prazos
                with ui.card().classes("w-full p-6 rounded-none shadow-sm bg-white border hairline"):
                    ui.label("Prazos desta candidatura").classes(
                        "font-display text-lg font-semibold text-[#16233D] mb-3"
                    )
                    deadlines = data.get("deadlines", [])
                    if not deadlines:
                        ui.label("Nenhum prazo cadastrado ainda.").classes(
                            "text-[#4B5563]/50 text-sm font-mono"
                        )
                    for d in deadlines:
                        with ui.row().classes(
                            "w-full justify-between items-center py-2 border-b hairline"
                        ):
                            ui.label(d["label"]).classes("text-[#16233D]")
                            ui.label(d["due_date"]).classes("font-mono text-[#A6402F] text-sm")

                # checklist
                with ui.card().classes("w-full p-6 rounded-none shadow-sm bg-white border hairline"):
                    ui.label("Checklist de documentos").classes(
                        "font-display text-lg font-semibold text-[#16233D] mb-3"
                    )
                    checklist = data.get("checklist", [])

                    def make_toggle_handler(item_key, checkbox):
                        async def handler(e):
                            result = await toggle_application_checklist_item(token, application_id, item_key)
                            if result is None:
                                checkbox.value = not e.value  # revert on failure
                                ui.notify("Erro ao atualizar item.", color="negative")
                        return handler

                    for item in checklist:
                        with ui.row().classes("w-full items-center py-1"):
                            cb = ui.checkbox(item["label"], value=item["completed"])
                            cb.on_value_change(make_toggle_handler(item["key"], cb))

        ui.timer(0, load, once=True)
