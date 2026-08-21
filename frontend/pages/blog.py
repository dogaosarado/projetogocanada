# pages/blog.py
#
# Antes desta sessão, esta página não tinha nav (só o logo) nem footer —
# única página do site nessa condição. Agora usa o mesmo header/footer
# compartilhados das demais.

from nicegui import ui
from pages.layout import design_tokens, site_header, site_footer
from frontend.services.api import get_posts, get_post


def blog_list_page() -> None:
    design_tokens()

    with ui.column().classes("w-full min-h-screen bg-[#F5F0E6] font-body"):
        site_header("blog")

        with ui.column().classes("w-full items-center py-16 px-4 flex-grow"):
            with ui.row().classes(
                "w-full max-w-3xl justify-between items-center mb-8"
            ):
                ui.label("Blog GoCanadaBR").classes(
                    "font-display text-3xl font-semibold text-[#16233D]"
                )

            content = ui.column().classes("w-full items-center")

        site_footer()

        async def load():
            posts = await get_posts()

            with content:
                if not posts:
                    ui.label("Nenhum post publicado ainda.").classes(
                        "text-[#4B5563]/50 font-mono text-sm"
                    )
                    return

                with ui.column().classes("w-full max-w-3xl gap-4"):
                    for post in posts:
                        with ui.card().classes(
                            "w-full p-6 rounded-none shadow-sm bg-white cursor-pointer "
                            "hover:shadow-md"
                        ).on(
                            "click",
                            lambda p=post: ui.navigate.to(f"/blog/{p['slug']}"),
                        ):
                            ui.label(post["title"]).classes(
                                "text-[#16233D] font-semibold text-xl"
                            )
                            ui.label(post["created_at"][:10]).classes(
                                "text-[#4B5563]/50 text-sm font-mono"
                            )

        ui.timer(0, load, once=True)


def blog_post_page(slug: str) -> None:
    design_tokens()

    with ui.column().classes("w-full min-h-screen bg-[#F5F0E6] font-body"):
        site_header("blog")

        with ui.column().classes("w-full items-center py-16 px-4 flex-grow"):
            with ui.column().classes("w-full max-w-2xl"):
                ui.button(
                    "← Voltar ao blog", on_click=lambda: ui.navigate.to("/blog")
                ).classes(
                    "bg-[#16233D] text-[#F5F0E6] rounded-none px-4 py-2 mb-6 "
                    "font-mono text-xs tracking-wide self-start"
                )

                content = ui.column().classes("w-full")

        site_footer()

        async def load():
            post = await get_post(slug)

            with content:
                if not post:
                    with ui.card().classes("w-full p-8 rounded-none text-center"):
                        ui.label("Post não encontrado.").classes(
                            "text-[#A6402F] font-mono"
                        )
                else:
                    with ui.card().classes(
                        "w-full p-8 rounded-none shadow-sm bg-white"
                    ):
                        ui.label(post["title"]).classes(
                            "font-display text-3xl font-semibold text-[#16233D] mb-2"
                        )
                        ui.label(post["created_at"][:10]).classes(
                            "text-[#4B5563]/50 text-sm font-mono mb-6"
                        )
                        with ui.element("div").classes("blog-content w-full"):
                            ui.html(post["body_html"])

        ui.timer(0, load, once=True)
