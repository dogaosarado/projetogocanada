# pages/form.py

from nicegui import ui
from state.user import get_token, get_tier, is_logged_in
from services.api import get_universities, submit_request
from state.user import logout


TIER_LIMITS = {
    "basico": 2,
    "intermediario": 3,
    "avancado": 4,
}


def form_page() -> None:
    if not is_logged_in():
        ui.navigate.to("/login")
        return

    token = get_token()
    tier = get_tier()
    max_universities = TIER_LIMITS.get(tier, 2)

    universities_data = get_universities(token) or []
    university_map = {u["name"]: u["departments"] for u in universities_data}
    university_names = sorted(university_map.keys())

    selections = []

    with ui.column().classes("w-full min-h-screen bg-stone-50 items-center py-12 px-4"):
        with ui.card().classes("w-full max-w-2xl p-8 shadow-lg rounded-2xl bg-white"):
            ui.label("GoCanada").classes("text-2xl font-bold text-amber-700 mb-1")
            add_logout_button()
            ui.label(
                f"Plano {tier.capitalize()} — selecione até {max_universities} universidade(s)"
            ).classes("text-stone-500 mb-6")

            with ui.column().classes("w-full gap-6"):
                for i in range(max_universities):
                    selected = {
                        "university": None,
                        "department": None,
                        "url": None,
                        "is_custom": False,
                    }
                    selections.append(selected)

                    with ui.card().classes("w-full p-4 bg-stone-50 rounded-xl"):
                        ui.label(f"Universidade {i + 1}").classes(
                            "text-stone-600 font-medium mb-3"
                        )

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

                        ui.select(
                            options=university_names,
                            label="Universidade",
                            on_change=make_univ_handler(selected, dept_select, custom_input),
                        ).classes("w-full")

                        dept_select.on_value_change(make_dept_handler(selected, custom_input))
                        custom_input.on_value_change(make_custom_handler(selected))

            ui.separator().classes("my-4")

            research = ui.textarea(
                "Interesses de pesquisa (opcional)",
                placeholder="Descreva brevemente suas áreas de interesse...",
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

                result = submit_request(token, payload)
                if result:
                    ui.navigate.to("/confirmacao")
                else:
                    error_label.text = "Erro ao enviar. Tente novamente."
                    error_label.set_visibility(True)

            ui.button("Enviar pedido", on_click=handle_submit).classes(
                "w-full mt-6 bg-amber-600 text-white rounded-xl py-2 hover:bg-amber-700"
            )
def add_logout_button():
    ui.button('Logoff', on_click=lambda: (logout(), ui.navigate.to('/login'))).props('flat color=negative')