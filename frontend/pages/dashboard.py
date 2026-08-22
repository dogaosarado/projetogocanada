# pages/dashboard.py

from nicegui import ui
from state.user import get_token, is_logged_in
from frontend.services.api import get_dashboard, change_password, get_meus_servicos
from pages.layout import design_tokens, authenticated_header
from state.user import must_change_password as must_change_password_state
async def dashboard_page() -> None:
    design_tokens()
    if not is_logged_in():
        ui.navigate.to("/login")
        return
    if must_change_password_state():
        ui.navigate.to("/trocar-senha")
        return
    token = get_token()
    data = await get_dashboard(token)

    with ui.column().classes("w-full min-h-screen bg-[#F5F0E6] font-body items-center py-8 px-4"):
        authenticated_header()

        if not data:
            with ui.card().classes("w-full max-w-2xl p-8 mt-6 rounded-none border hairline text-center"):
                ui.label("Erro ao carregar seu painel. Tente novamente mais tarde.").classes(
                    "text-red-500"
                )
            return

        with ui.column().classes("w-full max-w-3xl gap-6 mt-4"):

            # plano + conta
            with ui.card().classes("w-full p-6 rounded-none shadow-sm bg-white border hairline"):
                with ui.row().classes("w-full justify-between items-center flex-wrap gap-3"):
                    ui.label(f"Plano {data['tier'].capitalize()}").classes(
                        "font-display text-xl font-semibold text-[#A6402F]"
                    )
                    with ui.row().classes("gap-2"):
                        if not data.get("applications"):
                            ui.button(
                                "Preencher formulário de universidades",
                                on_click=lambda: ui.navigate.to("/formulario"),
                            ).classes(
                                "bg-[#A6402F] text-[#F5F0E6] rounded-none px-4 py-2 "
                                "font-mono text-xs tracking-wide hover:bg-[#8a3327]"
                            )
                        ui.button(
                            "Alterar senha",
                            on_click=lambda: open_password_dialog(token),
                        ).classes(
                            "bg-white border border-[#16233D]/20 text-[#16233D] rounded-none "
                            "px-4 py-2 font-mono text-xs tracking-wide hover:bg-[#F5F0E6]"
                        )
            # serviços contratados — relatório / mentoria, independente de data['tier']
            servicos = await get_meus_servicos(token) or []
            faltando = {"relatorio", "mentoria"} - set(servicos)

            if faltando:
                with ui.card().classes("w-full p-6 rounded-none shadow-sm bg-white border hairline"):
                    ui.label("Outros serviços").classes(
                        "font-display text-lg font-semibold text-[#16233D] mb-3"
                    )
                    ui.label("Você ainda não tem os seguintes serviços:").classes(
                        "text-[#4B5563]/60 text-sm font-mono mb-3"
                    )
                    with ui.row().classes("gap-2"):
                        if "relatorio" in faltando:
                            ui.button(
                                "Contratar Relatório",
                                on_click=lambda: ui.navigate.to("/relatorio/adicionar"),
                            ).classes(
                                "bg-[#A6402F] text-[#F5F0E6] rounded-none px-4 py-2 "
                                "font-mono text-xs tracking-wide hover:bg-[#8a3327]"
                            )
                        if "mentoria" in faltando:
                            ui.button(
                                "Contratar Mentoria",
                                on_click=lambda: ui.navigate.to("/mentoria/adicionar"),
                            ).classes(
                                "bg-[#A6402F] text-[#F5F0E6] rounded-none px-4 py-2 "
                                "font-mono text-xs tracking-wide hover:bg-[#8a3327]"
                            )

            # reuniões (gerais, não vinculadas a uma universidade específica)
            with ui.card().classes("w-full p-6 rounded-none shadow-sm bg-white border hairline"):
                ui.label("Reuniões com o consultor").classes(
                    "font-display text-lg font-semibold text-[#16233D] mb-3"
                )
                meetings = data.get("meetings", [])
                if not meetings:
                    ui.label("Nenhuma reunião agendada ainda.").classes(
                        "text-[#4B5563]/50 text-sm font-mono"
                    )
                for m in meetings:
                    with ui.row().classes(
                        "w-full justify-between items-center py-2 border-b hairline"
                    ):
                        with ui.column().classes("gap-0"):
                            ui.label(m["title"]).classes("text-[#16233D] font-medium")
                            if m.get("notes"):
                                ui.label(m["notes"]).classes("text-[#4B5563]/60 text-sm")
                        ui.label(m["scheduled_at"].replace("T", " ")[:16]).classes(
                            "text-[#A6402F] font-mono text-sm"
                        )

            # candidaturas — uma "caixa" por universidade/programa
            with ui.card().classes("w-full p-6 rounded-none shadow-sm bg-white border hairline"):
                ui.label("Suas candidaturas").classes(
                    "font-display text-lg font-semibold text-[#16233D] mb-4"
                )
                applications = data.get("applications", [])

                if not applications:
                    ui.label(
                        "Nenhuma candidatura ainda — preencha o formulário de universidades acima."
                    ).classes("text-[#4B5563]/50 text-sm font-mono")
                else:
                    with ui.grid(columns="repeat(auto-fill, minmax(220px, 1fr))").classes("w-full gap-4"):
                        for a in applications:
                            done = a["checklist_done"]
                            total = a["checklist_total"]
                            with ui.card().classes(
                                "p-5 rounded-none bg-[#F5F0E6] hover:bg-white hover:shadow-md "
                                "cursor-pointer transition-all border hairline"
                            ).on("click", lambda app_id=a["id"]: ui.navigate.to(f"/painel/candidatura/{app_id}")):
                                if a.get("is_custom"):
                                    ui.label("Personalizada").classes(
                                        "font-mono text-[10px] text-[#A6402F] tracking-widest uppercase mb-1"
                                    )
                                ui.label(a["university"]).classes(
                                    "font-display text-[#16233D] font-semibold text-lg"
                                )
                                ui.label(a["department"]).classes("text-[#4B5563] text-sm mb-3")
                                with ui.row().classes("w-full justify-between items-center text-xs"):
                                    ui.label(f"{a['deadline_count']} prazo(s)").classes(
                                        "font-mono text-[#4B5563]/50"
                                    )
                                    ui.label(f"{done}/{total} documentos").classes(
                                        "font-mono text-[#A6402F]"
                                    )


def open_password_dialog(token: str) -> None:
    with ui.dialog() as dialog, ui.card().classes("p-6 gap-3 rounded-none border hairline"):
        ui.label("Alterar senha").classes("font-display text-lg font-semibold text-[#16233D]")
        current = ui.input("Senha atual", password=True).classes("w-full")
        new = ui.input("Nova senha", password=True).classes("w-full")
        confirm = ui.input("Confirmar nova senha", password=True).classes("w-full")
        msg = ui.label("").classes("text-sm")
        msg.set_visibility(False)

        async def handle_submit():
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
            ok, text = await change_password(token, current.value, new.value)
            if ok:
                ui.notify("Senha alterada com sucesso.", color="positive")
                dialog.close()
            else:
                msg.text = text
                msg.classes(replace="text-sm text-red-500")
                msg.set_visibility(True)

        with ui.row().classes("gap-2 justify-end w-full mt-2"):
            ui.button("Cancelar", on_click=dialog.close).classes(
                "bg-white border border-[#16233D]/20 text-[#16233D] rounded-none px-4 py-2 "
                "font-mono text-xs tracking-wide hover:bg-[#F5F0E6]"
            )
            ui.button("Salvar", on_click=handle_submit).classes(
                "bg-[#A6402F] text-[#F5F0E6] rounded-none px-4 py-2 font-mono text-xs "
                "tracking-wide hover:bg-[#8a3327]"
            )
    dialog.open()
