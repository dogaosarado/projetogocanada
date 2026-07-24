# pages/blog.py

from nicegui import ui
from services.api import get_posts, get_post


def blog_list_page() -> None:
    posts = get_posts()

    with ui.column().classes("w-full min-h-screen bg-stone-50 items-center py-12 px-4"):
        with ui.row().classes("w-full max-w-3xl justify-between items-center mb-8"):
            ui.label("Blog GoCanadaBR").classes("text-3xl font-bold text-amber-700")
            ui.button("Voltar", on_click=lambda: ui.navigate.to("/")).classes(
                "bg-stone-200 text-stone-700 rounded-xl px-4 py-2"
            )

        if not posts:
            ui.label("Nenhum post publicado ainda.").classes("text-stone-400")

        with ui.column().classes("w-full max-w-3xl gap-4"):
            for post in posts:
                with ui.card().classes("w-full p-6 rounded-2xl shadow-sm bg-white cursor-pointer hover:shadow-md") \
                        .on("click", lambda p=post: ui.navigate.to(f"/blog/{p['slug']}")):
                    ui.label(post["title"]).classes("text-xl font-bold text-stone-800")
                    ui.label(post["created_at"][:10]).classes("text-stone-400 text-sm")


def blog_post_page(slug: str) -> None:
    post = get_post(slug)

    with ui.column().classes("w-full min-h-screen bg-stone-50 items-center py-12 px-4"):
        with ui.column().classes("w-full max-w-2xl"):
            ui.button("← Voltar ao blog", on_click=lambda: ui.navigate.to("/blog")).classes(
                "bg-stone-200 text-stone-700 rounded-xl px-4 py-2 mb-6 self-start"
            )

            if not post:
                with ui.card().classes("w-full p-8 text-center"):
                    ui.label("Post não encontrado.").classes("text-red-500")
                return

            with ui.card().classes("w-full p-8 rounded-2xl shadow-sm bg-white"):
                ui.label(post["title"]).classes("text-3xl font-bold text-stone-800 mb-2")
                ui.label(post["created_at"][:10]).classes("text-stone-400 text-sm mb-6")
                ui.html(post["body_html"])