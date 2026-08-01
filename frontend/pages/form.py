# pages/form.py

from nicegui import ui
from state.user import get_token, get_tier, is_logged_in, must_change_password
from services.api import get_universities, submit_request, get_request_status
from pages.layout import design_tokens, authenticated_header


TIER_LIMITS = {
    "relatorio_gratis": 1,
    "relatorio_basico": 2,
    "relatorio_intermediario": 3,
    "relatorio_avancado": 4,
}


def form_page() -> None:
    design_tokens()
    if not is_logged_in():
        ui.navigate.to("/login")
        return
    if must_change_password():
        ui.navigate.to("/trocar-senha")
        return

    token = get_token()
    tier = get_tier()
    max_universities = TIER_LIMITS.get(tier, 2)

    if get_request_status(token):
        with ui.column().classes(
            "w-full min-h-screen bg-[#F5F0E6] font-body items-center py-12 px-4"
        ):
            authenticated_header()
            with ui.card().classes(
                "w-full max-w-2xl p-8 shadow-md rounded-none bg-white border hairline text-center"
            ):
                ui.label("Formulário já enviado").classes(
                    "font-display text-2xl font-semibold text-[#A6402F] mb-3"
                )
                ui.label(
                    "Você já enviou seu formulário de universidades e programas. "
                    "Para alterar suas escolhas, entre em contato com a equipe GoCanadaBR "
                    "pelo contato@gocanadabr.com.br."
                ).classes("text-[#4B5563]")
                ui.button("Voltar ao painel", on_click=lambda: ui.navigate.to("/painel")).classes(
                    "bg-[#A6402F] text-[#F5F0E6] rounded-none px-5 py-2 mt-6 "
                    "font-mono text-xs tracking-wide hover:bg-[#8a3327]"
                )
        return

    universities_data = get_universities(token) or []
    university_map = {u["name"]: u["departments"] for u in universities_data}
    university_names = sorted(university_map.keys())

    selections = []

    with ui.column().classes(
        "w-full min-h-screen bg-[#F5F0E6] font-body items-center py-12 px-4"
    ):
        authenticated_header()
        with ui.card().classes(
            "w-full max-w-2xl p-8 shadow-md rounded-none bg-white border hairline"
        ):
            ui.label("GoCanadaBR").classes(
                "font-display text-2xl font-semibold text-[#A6402F] mb-1"
            )
            ui.label(
                f"Plano {tier.capitalize()} — selecione até {max_universities} universidade(s)"
            ).classes("text-[#4B5563] mb-6 font-mono text-sm")

            with ui.column().classes("w-full gap-6"):
                for i in range(max_universities):
                    selected = {
                        "university": None,
                        "department": None,
                        "url": None,
                        "is_custom": False,
                    }
                    selections.append(selected)

                    with ui.card().classes(
                        "w-full p-4 bg-[#F5F0E6] rounded-none border hairline"
                    ):
                        ui.label(f"Universidade {i + 1}").classes(
                            "text-[#16233D] font-mono text-xs tracking-wide mb-3"
                        )

                        univ_select_container = ui.column().classes("w-full")

                        dept_select = ui.select(
                            options={},
                            label="Programa de pós-graduação",
                        ).classes("w-full mt-3")
                        dept_select.set_visibility(False)

                        custom_input = ui.input(
                            placeholder="Não encontrou o departamento desejado? Escreva aqui."
                        ).classes("w-full mt-3")
                        custom_input.set_visibility(False)

                        def make_univ_handler(sel, ds, ci):
                            def handler(e):
                                sel["university"] = e.value
                                sel["department"] = None
                                sel["url"] = None
                                sel["is_custom"] = False
                                depts = university_map.get(e.value, [])
                                options = {d["name"]: d["name"] for d in depts}
                                ds.options = options
                                ds.value = None
                                ds.set_visibility(True)
                                ci.set_visibility(True)
                                ds.update()
                            return handler

                        def make_dept_handler(sel, ci):
                            def handler(e):
                                if not e.value:
                                    return
                                sel["is_custom"] = False
                                sel["department"] = e.value
                                univ = sel.get("university")
                                depts = university_map.get(univ, [])
                                match = next(
                                    (d for d in depts if d["name"] == e.value), None
                                )
                                sel["url"] = match["url"] if match else None
                            return handler

                        def make_custom_handler(sel):
                            def handler(e):
                                if e.value.strip():
                                    sel["department"] = e.value.strip()
                                    sel["url"] = None
                                    sel["is_custom"] = True
                            return handler

                        with univ_select_container:
                            ui.select(
                                options=university_names,
                                label="Universidade",
                                on_change=make_univ_handler(selected, dept_select, custom_input),
                            ).classes("w-full")

                        dept_select.on_value_change(make_dept_handler(selected, custom_input))
                        custom_input.on_value_change(make_custom_handler(selected))

            ui.element("div").classes("h-px w-full bg-[#B8925A55] my-4")

            research = ui.textarea(
                "Currículo lattes (opcional)",
                placeholder="Se desejar fornecer mais contexto, cole o link de seu lattes.",
            ).classes("w-full")

            error_label = ui.label("").classes("text-red-500 text-sm")
            error_label.set_visibility(False)

            def handle_submit():
                filled = [
                    s for s in selections
                    if s.get("university") and s.get("department")
                ]
                if not filled:
                    error_label.text = "Selecione ao menos uma universidade e um departamento."
                    error_label.set_visibility(True)
                    return

                payload = {
                    "universities_selected": filled,
                    "research_interests": research.value or None,
                }

                result, error = submit_request(token, payload)
                if result:
                    ui.navigate.to("/confirmacao")
                else:
                    error_label.text = error or "Erro ao enviar. Tente novamente."
                    error_label.set_visibility(True)

            ui.button("Enviar pedido", on_click=handle_submit).classes(
                "w-full mt-6 bg-[#A6402F] text-[#F5F0E6] rounded-none py-2 "
                "font-mono text-sm tracking-wide hover:bg-[#8a3327]"
            )
