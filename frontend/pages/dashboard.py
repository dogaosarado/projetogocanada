# pages/dashboard.py

from nicegui import ui
from state.user import get_token, is_logged_in
from services.api import get_dashboard, change_password
from pages.layout import authenticated_header
from state.user import must_change_password as must_change_password_state

def dashboard_page() -> None:
    if not is_logged_in():
        ui.navigate.to("/login")
        return
    if must_change_password_state():
        ui.navigate.to("/trocar-senha")
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

        with ui.column().classes("w-full max-w-3xl gap-6 mt-4"):

            # plano + conta
            with ui.card().classes("w-full p-6 rounded-2xl shadow-sm bg-white"):
                with ui.row().classes("w-full justify-between items-center flex-wrap gap-3"):
                    ui.label(f"Plano {data['tier'].capitalize()}").classes(
                        "text-xl font-bold text-amber-700"
                    )
                    with ui.row().classes("gap-2"):
                        if not data.get("applications"):
                            ui.button(
                                "Preencher formulário de universidades",
                                on_click=lambda: ui.navigate.to("/formulario"),
                            ).classes("bg-amber-600 text-white rounded-xl px-4 py-2 hover:bg-amber-700")
                        ui.button(
                            "Alterar senha",
                            on_click=lambda: open_password_dialog(token),
                        ).classes("bg-stone-200 text-stone-700 rounded-xl px-4 py-2")

            # reuniões (gerais, não vinculadas a uma universidade específica)
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

            # candidaturas — uma "caixa" por universidade/programa
            with ui.card().classes("w-full p-6 rounded-2xl shadow-sm bg-white"):
                ui.label("Suas candidaturas").classes("text-lg font-bold text-stone-800 mb-4")
                applications = data.get("applications", [])

                if not applications:
                    ui.label(
                        "Nenhuma candidatura ainda — preencha o formulário de universidades acima."
                    ).classes("text-stone-400 text-sm")
                else:
                    with ui.grid(columns="repeat(auto-fill, minmax(220px, 1fr))").classes("w-full gap-4"):
                        for a in applications:
                            done = a["checklist_done"]
                            total = a["checklist_total"]
                            with ui.card().classes(
                                "p-5 rounded-2xl bg-stone-50 hover:bg-amber-50 hover:shadow-md "
                                "cursor-pointer transition-all border border-stone-100"
                            ).on("click", lambda app_id=a["id"]: ui.navigate.to(f"/painel/candidatura/{app_id}")):
                                if a.get("is_custom"):
                                    ui.label("Personalizada").classes(
                                        "text-xs text-amber-600 font-semibold uppercase mb-1"
                                    )
                                ui.label(a["university"]).classes("text-stone-800 font-bold text-lg")
                                ui.label(a["department"]).classes("text-stone-500 text-sm mb-3")
                                with ui.row().classes("w-full justify-between items-center text-xs"):
                                    ui.label(f"{a['deadline_count']} prazo(s)").classes("text-stone-400")
                                    ui.label(f"{done}/{total} documentos").classes(
                                        "text-amber-700 font-medium"
                                    )


def open_password_dialog(token: str) -> None:
    with ui.dialog() as dialog, ui.card().classes("p-6 gap-3 rounded-2xl"):
        ui.label("Alterar senha").classes("text-lg font-bold text-stone-800")
        current = ui.input("Senha atual", password=True).classes("w-full")
        new = ui.input("Nova senha", password=True).classes("w-full")
        confirm = ui.input("Confirmar nova senha", password=True).classes("w-full")
        msg = ui.label("").classes("text-sm")
        msg.set_visibility(False)

        def handle_submit():
            if not current.value or not new.value:
                msg.text = "Preencha todos os campos."
                msg.classes(replace="text-sm text-red-500")
                msg.set_visibility(True)
                return
            if new.value != confirm.value:
                msg.text = "As senhas novas não coincidem."
                msg.classes(replace="text-sm text-red-500")
                msg.set_visibility(True)
                return
            ok, text = change_password(token, current.value, new.value)
            if ok:
                ui.notify("Senha alterada com sucesso.", color="positive")
                dialog.close()
            else:
                msg.text = text
                msg.classes(replace="text-sm text-red-500")
                msg.set_visibility(True)

        with ui.row().classes("gap-2 justify-end w-full mt-2"):
            ui.button("Cancelar", on_click=dialog.close).classes("bg-stone-200 text-stone-700 rounded-xl px-4 py-2")
            ui.button("Salvar", on_click=handle_submit).classes(
                "bg-amber-600 text-white rounded-xl px-4 py-2 hover:bg-amber-700"
            )
    dialog.open()
