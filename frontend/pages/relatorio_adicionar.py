# pages/relatorio_adicionar.py

from nicegui import ui
from pages.layout import design_tokens, authenticated_header
from frontend.services.api import get_universities_public, adicionar_servico_relatorio
from state.user import get_token, is_logged_in

REPORT_UNIVERSITY_LIMITS = {
    "relatorio_gratis": 1,
    "relatorio_basico": 2,
    "relatorio_intermediario": 3,
    "relatorio_avancado": 4,
}

TIER_LABELS = {
    "relatorio_gratis": "Grátis",
    "relatorio_basico": "Básico",
    "relatorio_intermediario": "Intermediário",
    "relatorio_avancado": "Avançado",
}


async def relatorio_adicionar_page(tier: str = "relatorio_gratis") -> None:
    design_tokens()
    if not is_logged_in():
        ui.navigate.to("/login")
        return

    if tier not in REPORT_UNIVERSITY_LIMITS:
        tier = "relatorio_gratis"

    max_universities = REPORT_UNIVERSITY_LIMITS[tier]
    token = get_token()
    universities_data = await get_universities_public() or []
    university_map = {u["name"]: u["departments"] for u in universities_data}
    university_names = sorted(university_map.keys())

    selections = []

    with ui.column().classes("w-full min-h-screen bg-[#F5F0E6] font-body items-center py-8 px-4"):
        authenticated_header()

        with ui.column().classes("w-full items-center py-4 px-4"):
            with ui.card().classes(
                "w-full max-w-2xl p-8 shadow-md rounded-none bg-white border hairline"
            ):
                ui.label("Contratar Relatório").classes(
                    "font-display text-2xl font-semibold text-[#A6402F] mb-1"
                )
                ui.label(f"Plano {TIER_LABELS.get(tier, tier)}").classes(
                    "text-[#4B5563] mb-6 font-mono text-sm"
                )

                ui.label(
                    f"Universidades e programas de interesse (até {max_universities})"
                ).classes("text-[#4B5563] text-sm mb-3")

                for i in range(max_universities):
                    selected = {"university": None, "department": None, "url": None, "is_custom": False}
                    selections.append(selected)

                    with ui.card().classes(
                        "w-full p-4 bg-[#F5F0E6] rounded-none border hairline mb-3"
                    ):
                        ui.label(f"Universidade {i + 1}" + (" (opcional)" if i > 0 else "")).classes(
                            "text-[#16233D] font-mono text-xs tracking-wide mb-3"
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

                ui.element("div").classes("h-px w-full bg-[#B8925A55] my-4")
                lattes_input = ui.input(
                    "Link do currículo Lattes (opcional)",
                    placeholder="https://buscatextual.cnpq.br/...",
                ).classes("w-full")

                error_msg = ui.label("").classes("text-red-500 text-sm mt-2")
                error_msg.set_visibility(False)

                async def handle_submit():
                    filled = [s for s in selections if s.get("university") and s.get("department")]
                    if not filled:
                        error_msg.text = "Selecione ao menos uma universidade e um departamento."
                        error_msg.set_visibility(True)
                        return

                    payload = {
                        "tier": tier,
                        "universities_selected": filled,
                        "lattes_url": lattes_input.value.strip() or None,
                    }
                    result, error = await adicionar_servico_relatorio(token, payload)
                    if result:
                        ui.notify("Relatório adicionado à sua conta.", color="positive")
                        ui.navigate.to("/dashboard")
                    else:
                        error_msg.text = error or "Erro ao adicionar serviço. Tente novamente."
                        error_msg.set_visibility(True)

                ui.button("Contratar", on_click=handle_submit).classes(
                    "w-full mt-6 bg-[#A6402F] text-[#F5F0E6] rounded-none py-2 "
                    "font-mono text-sm tracking-wide hover:bg-[#8a3327]"
                )