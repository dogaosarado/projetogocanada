from nicegui import ui
from state.user import get_name, is_logged_in, logout


def authenticated_header() -> None:
    if not is_logged_in():
        return
    with ui.row().classes("w-full px-6 py-3 bg-white shadow-sm justify-between items-center"):
        name = get_name()
        ui.label(f"Bem-vindo(a), {name}" if name else "Bem-vindo(a)").classes(
            "text-stone-700 font-medium"
        )
        ui.button(
            "Sair",
            on_click=lambda: (logout(), ui.navigate.to("/login")),
        ).props("flat color=negative")