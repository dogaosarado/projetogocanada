# pages/mentoria_signup.py

from copy import error
from sqlalchemy.engine.result import result
from nicegui import ui
from pages.layout import brand_logo
from services.api import get_universities_public, mentoria_signup

MENTORSHIP_UNIVERSITY_LIMITS = {
    "mentoria_basico": 2,
    "mentoria_intermediario": 3,
    "mentoria_avancado": 4,
}

TIER_LABELS = {
    "mentoria_basico": "Básico",
    "mentoria_intermediario": "Intermediário",
    "mentoria_avancado": "Avançado",
}


def mentoria_signup_page(tier: str = "mentoria_basico") -> None:
    if tier not in MENTORSHIP_UNIVERSITY_LIMITS:
        tier = "mentoria_basico"

    max_universities = MENTORSHIP_UNIVERSITY_LIMITS[tier]
    universities_data = get_universities_public() or []
    university_map = {u["name"]: u["departments"] for u in universities_data}
    university_names = sorted(university_map.keys())

    selections = []

    with ui.column().classes("w-full min-h-screen bg-stone-50"):
        with ui.row().classes("w-full px-8 py-5 bg-white shadow-sm justify-start items-center"):
            brand_logo()

        with ui.column().classes("w-full items-center py-12 px-4"):
            with ui.card().classes("w-full max-w-2xl p-8 shadow-lg rounded-2xl bg-white"):
                ui.label("Cadastro — Mentoria").classes("text-2xl font-bold text-amber-700 mb-1")
                ui.label(f"Plano {TIER_LABELS.get(tier, tier)}").classes("text-stone-500 mb-6")

                name_input = ui.input("Nome completo").classes("w-full")
                email_input = ui.input("Email").classes("w-full mt-3")

                ui.separator().classes("my-4")
                ui.label(
                    f"Universidades e programas de interesse (até {max_universities}) — "
                    "isso não é o serviço de relatório, é só pra darmos contexto na mentoria."
                ).classes("text-stone-500 text-sm mb-3")

                for i in range(max_universities):
                    selected = {"university": None, "department": None, "url": None, "is_custom": False}
                    selections.append(selected)

                    with ui.card().classes("w-full p-4 bg-stone-50 rounded-xl mb-3"):
                        ui.label(f"Universidade {i + 1}" + (" (opcional)" if i > 0 else "")).classes(
                            "text-stone-600 font-medium mb-3"
                        )

                        dept_select = ui.select(options={}, label="Programa de pós-graduação").classes("w-full mt-3")
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
                                ds.options = {d["name"]: d["name"] for d in depts}
                                ds.value = None
                                ds.set_visibility(True)
                                ci.set_visibility(True)
                                ds.update()
                            return handler

                        def make_dept_handler(sel):
                            def handler(e):
                                if not e.value:
                                    return
                                sel["is_custom"] = False
                                sel["department"] = e.value
                                depts = university_map.get(sel.get("university"), [])
                                match = next((d for d in depts if d["name"] == e.value), None)
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
                        dept_select.on_value_change(make_dept_handler(selected))
                        custom_input.on_value_change(make_custom_handler(selected))

                ui.separator().classes("my-4")
                lattes_input = ui.textarea(
                    "Currículo lattes (opcional)",
                    placeholder="Se desejar fornecer mais contexto, cole o link de seu lattes.",
                ).classes("w-full")

                error_msg = ui.label("").classes("text-red-500 text-sm mt-2")
                error_msg.set_visibility(False)

                def handle_submit():
                    if not name_input.value.strip():
                        error_msg.text = "Informe seu nome."
                        error_msg.set_visibility(True)
                        return
                    if not email_input.value.strip():
                        error_msg.text = "Informe seu email."
                        error_msg.set_visibility(True)
                        return
                    filled = [s for s in selections if s.get("university") and s.get("department")]
                    if not filled:
                        error_msg.text = "Selecione ao menos uma universidade e um departamento."
                        error_msg.set_visibility(True)
                        return

                    payload = {
                        "name": name_input.value,
                        "email": email_input.value,
                        "tier": tier,
                        "universities_selected": filled,
                        "research_interests": lattes_input.value or None,
                    }
                    result, error = mentoria_signup(payload)
                    if result:
                        ui.navigate.to("/mentoria/interesse")
                    else:
                        error_msg.text = error or "Erro ao cadastrar. Tente novamente."
                        error_msg.set_visibility(True)

                ui.button("Enviar cadastro", on_click=handle_submit).classes(
                    "w-full mt-6 bg-amber-600 text-white rounded-xl py-2 hover:bg-amber-700"
                )