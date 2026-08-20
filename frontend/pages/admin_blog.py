# pages/admin_blog.py

import re
import markdown2
from nicegui import ui
from state.user import get_token, get_is_admin, is_logged_in
from frontend.services.api import (
    get_all_posts_admin,
    create_post_admin,
    update_post_admin,
    delete_post_admin,
)
from pages.layout import authenticated_header


def slugify(title: str) -> str:
    slug = title.strip().lower()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug).strip("-")
    return slug


def markdown_to_html(text: str) -> str:
    return markdown2.markdown(text, extras=["fenced-code-blocks", "tables", "cuddled-lists"])


def admin_blog_page() -> None:
    if not is_logged_in():
        ui.navigate.to("/login")
        return

    token = get_token()

    if not get_is_admin():
        ui.navigate.to("/")
        return

    posts = get_all_posts_admin(token)

    with ui.column().classes("w-full min-h-screen bg-stone-50 items-center py-12 px-4"):
        authenticated_header()
        with ui.card().classes("w-full max-w-4xl p-8 shadow-lg rounded-2xl bg-white"):
            with ui.row().classes("w-full justify-between items-center mb-6"):
                ui.label("Blog — Admin").classes("text-2xl font-bold text-amber-700")
                ui.button("← Voltar ao painel admin", on_click=lambda: ui.navigate.to("/admin")).classes(
                    "bg-stone-200 text-stone-700 rounded-xl px-4 py-2"
                )

            # criar post
            ui.label("Novo post").classes("text-lg font-semibold text-stone-700 mb-2")
            with ui.column().classes("w-full gap-3"):
                new_title = ui.input("Título").classes("w-full")
                new_slug = ui.input("Slug (URL)").classes("w-full")
                new_body = ui.textarea("Conteúdo (Markdown)").classes("w-full").props("rows=8")
                new_published = ui.checkbox("Publicar imediatamente", value=False)
                create_msg = ui.label("").classes("text-sm")
                create_msg.set_visibility(False)

                def suggest_slug():
                    if new_title.value and not new_slug.value:
                        new_slug.value = slugify(new_title.value)

                new_title.on("blur", lambda: suggest_slug())

                def handle_create():
                    if not new_title.value or not new_slug.value or not new_body.value:
                        create_msg.text = "Preencha título, slug e conteúdo."
                        create_msg.classes("text-red-500")
                        create_msg.set_visibility(True)
                        return
                    result = create_post_admin(
                        token,
                        new_title.value,
                        new_slug.value,
                        markdown_to_html(new_body.value),
                        new_published.value,
                    )
                    if result:
                        ui.navigate.to("/admin/blog")
                    else:
                        create_msg.text = "Erro ao criar post — slug pode já existir."
                        create_msg.classes("text-red-500")
                        create_msg.set_visibility(True)

                ui.button("Criar post", on_click=handle_create).classes(
                    "bg-amber-600 text-white rounded-xl px-5 py-2 hover:bg-amber-700 self-start"
                )

            ui.separator().classes("my-6")

            # lista de posts
            ui.label("Posts existentes").classes("text-lg font-semibold text-stone-700 mb-4")

            if not posts:
                ui.label("Nenhum post cadastrado.").classes("text-stone-400")
            else:
                with ui.column().classes("w-full gap-4"):
                    for post in posts:
                        with ui.expansion(
                            f"{post['title']}  —  /{post['slug']}  —  {'Publicado' if post['published'] else 'Rascunho'}"
                        ).classes("w-full bg-stone-50 rounded-xl px-4"):
                            with ui.column().classes("w-full gap-3 py-3"):
                                edit_title = ui.input("Título", value=post["title"]).classes("w-full")
                                edit_body = (
                                    ui.textarea(
                                        "Conteúdo (HTML já convertido — editar aqui é editar HTML, não Markdown)",
                                        value=post["body_html"],
                                    )
                                    .classes("w-full")
                                    .props("rows=8")
                                )
                                edit_published = ui.checkbox("Publicado", value=post["published"])
                                edit_msg = ui.label("").classes("text-sm")
                                edit_msg.set_visibility(False)

                                def handle_update(
                                    pid=post["id"], t=edit_title, b=edit_body, p=edit_published, msg=edit_msg
                                ):
                                    result = update_post_admin(
                                        token, pid, title=t.value, body_html=b.value, published=p.value
                                    )
                                    if result:
                                        ui.navigate.to("/admin/blog")
                                    else:
                                        msg.text = "Erro ao salvar."
                                        msg.classes("text-red-500")
                                        msg.set_visibility(True)

                                def handle_delete(pid=post["id"]):
                                    if delete_post_admin(token, pid):
                                        ui.navigate.to("/admin/blog")
                                    else:
                                        ui.notify("Erro ao deletar.", color="negative")

                                with ui.row().classes("gap-2"):
                                    ui.button("Salvar", on_click=handle_update).classes(
                                        "bg-amber-600 text-white rounded-xl px-4 py-2 hover:bg-amber-700"
                                    )
                                    ui.button("Deletar", on_click=handle_delete).classes(
                                        "bg-red-500 text-white rounded-xl px-4 py-2 hover:bg-red-600"
                                    )
