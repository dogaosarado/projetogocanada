# pages/form.py

from nicegui import ui
from state.user import get_token, get_tier, is_logged_in
from services.api import get_universities, submit_request


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
            ui.label(
                f"Plano {tier.capitalize()} — selecione até {max_universities} universidade(s)"
            ).classes("text-stone-500 mb-6")
            ui.html('''
<svg width="100%" viewBox="0 0 680 200" role="img" style="margin: 16px 0;">
<defs>
<marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
<path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
</marker>
</defs>
<rect x="40" y="60" width="130" height="56" rx="8" stroke-width="0.5" fill="#FAEEDA" stroke="#854F0B"/>
<text font-family="sans-serif" font-size="14" font-weight="500" x="105" y="83" text-anchor="middle" dominant-baseline="central" fill="#633806">Seus dados</text>
<text font-family="sans-serif" font-size="12" x="105" y="101" text-anchor="middle" dominant-baseline="central" fill="#854F0B">Nome, email e plano</text>
<line x1="170" y1="88" x2="196" y2="88" stroke="#BA7517" stroke-width="1.5" marker-end="url(#arrow)"/>
<rect x="196" y="60" width="130" height="56" rx="8" stroke-width="0.5" fill="#FAEEDA" stroke="#854F0B"/>
<text font-family="sans-serif" font-size="14" font-weight="500" x="261" y="83" text-anchor="middle" dominant-baseline="central" fill="#633806">Universidades</text>
<text font-family="sans-serif" font-size="12" x="261" y="101" text-anchor="middle" dominant-baseline="central" fill="#854F0B">Programas de interesse</text>
<line x1="326" y1="88" x2="352" y2="88" stroke="#BA7517" stroke-width="1.5" marker-end="url(#arrow)"/>
<rect x="352" y="60" width="130" height="56" rx="8" stroke-width="0.5" fill="#FAEEDA" stroke="#854F0B"/>
<text font-family="sans-serif" font-size="14" font-weight="500" x="417" y="83" text-anchor="middle" dominant-baseline="central" fill="#633806">Pagamento</text>
<text font-family="sans-serif" font-size="12" x="417" y="101" text-anchor="middle" dominant-baseline="central" fill="#854F0B">Pix — rápido e seguro</text>
<line x1="482" y1="88" x2="508" y2="88" stroke="#BA7517" stroke-width="1.5" marker-end="url(#arrow)"/>
<rect x="508" y="60" width="132" height="56" rx="8" stroke-width="0.5" fill="#E1F5EE" stroke="#0F6E56"/>
<text font-family="sans-serif" font-size="14" font-weight="500" x="574" y="83" text-anchor="middle" dominant-baseline="central" fill="#085041">Relatório</text>
<text font-family="sans-serif" font-size="12" x="574" y="101" text-anchor="middle" dominant-baseline="central" fill="#0F6E56">Entregue por email</text>
<text font-family="sans-serif" font-size="12" x="105" y="140" text-anchor="middle" fill="#888780">1</text>
<text font-family="sans-serif" font-size="12" x="261" y="140" text-anchor="middle" fill="#888780">2</text>
<text font-family="sans-serif" font-size="12" x="417" y="140" text-anchor="middle" fill="#888780">3</text>
<text font-family="sans-serif" font-size="12" x="574" y="140" text-anchor="middle" fill="#888780">4</text>
</svg>
''')

            selections_container = ui.column().classes("w-full gap-6")

            with selections_container:
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
                            "text-stone-600 font-medium mb-2"
                        )

                        dept_select = ui.select(
                            options={},
                            label="Programa",
                        ).classes("w-full mt-2")
                        dept_select.set_visibility(False)

                        custom_input = ui.input("Digite o programa").classes("w-full mt-2")
                        custom_input.set_visibility(False)

                        def make_univ_handler(sel, ds, ci, idx):
                            def handler(e):
                                sel["university"] = e.value
                                sel["department"] = None
                                sel["url"] = None
                                sel["is_custom"] = False
                                depts = university_map.get(e.value, [])
                                options = {d["name"]: d["name"] for d in depts}
                                options["Outro (digitar manualmente)"] = "__custom__"
                                ds.options = options
                                ds.value = None
                                ds.set_visibility(True)
                                ci.set_visibility(False)
                                ds.update()
                            return handler

                        def make_dept_handler(sel, ci, univ_getter):
                            def handler(e):
                                if e.value == "__custom__":
                                    sel["department"] = None
                                    sel["url"] = None
                                    sel["is_custom"] = True
                                    ci.set_visibility(True)
                                else:
                                    sel["is_custom"] = False
                                    sel["department"] = e.value
                                    ci.set_visibility(False)
                                    univ = sel.get("university")
                                    depts = university_map.get(univ, [])
                                    match = next(
                                        (d for d in depts if d["name"] == e.value), None
                                    )
                                    sel["url"] = match["url"] if match else None
                            return handler

                        def make_custom_handler(sel):
                            def handler(e):
                                sel["department"] = e.value
                                sel["url"] = None
                            return handler

                        univ_select = ui.select(
                            options=university_names,
                            label="Universidade",
                            on_change=make_univ_handler(selected, dept_select, custom_input, i),
                        ).classes("w-full")

                        dept_select.on_value_change(
                            make_dept_handler(selected, custom_input, lambda s=selected: s.get("university"))
                        )
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
                    error_label.text = "Selecione ao menos uma universidade e um programa."
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