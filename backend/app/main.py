# app/main.py

import os
import sys

# backend/app/main.py -> sobe dois níveis pra chegar em projetogocanada/,
# onde `frontend/` mora como pasta irmã de `backend/`. Sem isso, `import
# frontend.pages...` não resolve nem rodando o uvicorn de dentro de backend/.
_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

_FRONTEND_ROOT = os.path.join(_PROJECT_ROOT, "frontend")
if _FRONTEND_ROOT not in sys.path:
    sys.path.insert(0, _FRONTEND_ROOT)

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from nicegui import ui

from app.routers import admin, auth, requests, universities, blog, dashboard, mentoria, relatorio_signup, relatorio

app = FastAPI(
    title="GoCanadaBR Consultoria",
    version="1.0.0",
    docs_url="/docs" if True else None,
)

# CORS removido: frontend e backend agora são a mesma origem, o middleware
# não faz mais nada além de trabalho extra por request.

app.include_router(auth.router)
app.include_router(universities.router)
app.include_router(requests.router)
app.include_router(admin.router)
app.include_router(blog.router)
app.include_router(dashboard.router)
app.include_router(mentoria.router)
app.include_router(relatorio_signup.router)
app.include_router(relatorio.router)


@app.get("/health")
def health():
    return {"status": "ok"}


# --- NiceGUI montado no mesmo app FastAPI, mesma porta, mesmo processo ---

app.mount(
    "/assets",
    StaticFiles(directory=os.path.join(_PROJECT_ROOT, "frontend", "assets")),
    name="assets",
)

ui.add_head_html('''
<style>
.q-menu,
.q-position-engine,
body > .q-menu,
.q-select__dialog {
    z-index: 9999 !important;
}
.q-card {
    overflow: visible !important;
}
</style>
''', shared=True)

from frontend.pages.relatorio import relatorio_page
from frontend.pages.mentoria import mentoria_page
from frontend.pages.contact import contact_page
from frontend.pages.login import login_page
from frontend.pages.form import form_page
from frontend.pages.confirmation import confirmation_page
from frontend.pages.admin import admin_page
from frontend.pages.admin_relatorio import admin_relatorio_page
from frontend.pages.interest import interest_page
from frontend.pages.dashboard import dashboard_page
from frontend.pages.blog import blog_list_page, blog_post_page
from frontend.pages.admin_client import admin_client_page
from frontend.pages.admin_blog import admin_blog_page
from frontend.pages.application_detail import application_detail_page
from frontend.pages.about import about_page
from frontend.pages.mentoria_signup import mentoria_signup_page
from frontend.pages.relatorio_signup import relatorio_signup_page
from frontend.pages.relatorio_interest import relatorio_interest_page
from frontend.pages.change_password_forced import change_password_forced_page
from frontend.pages.mentoria_interest import mentoria_interest_page
from frontend.pages.mentoria_adicionar import mentoria_adicionar_page
from frontend.pages.relatorio_adicionar import relatorio_adicionar_page


@ui.page("/interesse")
def interesse():
    interest_page()

@ui.page("/admin")
def admin_page_route():
    admin_page()

@ui.page("/admin/relatorio")
def admin_relatorio():
    admin_relatorio_page()

@ui.page("/")
def index():
    mentoria_page()

@ui.page("/relatorio")
async def relatorio_route():
    await relatorio_page()

@ui.page("/contato")
def contato():
    contact_page()

@ui.page("/mentoria")
def mentoria_redirect():
    ui.navigate.to("/")

@ui.page("/login")
def login():
    login_page()

@ui.page("/formulario")
async def formulario():
    await form_page()

@ui.page("/confirmacao")
def confirmacao():
    confirmation_page()

@ui.page("/painel")
async def painel():
    await dashboard_page()

@ui.page("/blog")
def blog():
    blog_list_page()

@ui.page("/blog/{slug}")
def blog_post(slug: str):
    blog_post_page(slug)

@ui.page("/admin/users/{user_id}")
def admin_client(user_id: int):
    admin_client_page(user_id)

@ui.page("/admin/blog")
def admin_blog():
    admin_blog_page()

@ui.page("/painel/candidatura/{application_id}")
def painel_candidatura(application_id: int):
    application_detail_page(application_id)

@ui.page("/quem-somos")
def quem_somos():
    about_page()

@ui.page("/mentoria/interesse")
def mentoria_interesse():
    mentoria_interest_page()

@ui.page("/mentoria/cadastro")
async def mentoria_cadastro(tier: str = "mentoria_basico"):
    await mentoria_signup_page(tier)

@ui.page("/relatorio/interesse")
def relatorio_interesse():
    relatorio_interest_page()

@ui.page("/relatorio/cadastro")
async def relatorio_cadastro(tier: str = "relatorio_gratis"):
    await relatorio_signup_page(tier)

@ui.page("/trocar-senha")
def trocar_senha():
    change_password_forced_page()

@ui.page("/relatorio/adicionar")
async def relatorio_adicionar(tier: str = "relatorio_gratis"):
    await relatorio_adicionar_page(tier)

@ui.page("/mentoria/adicionar")
async def mentoria_adicionar(tier: str = "mentoria_basico"):
    await mentoria_adicionar_page(tier)


ui.run_with(
    app,
    mount_path="/",
    storage_secret=os.environ["STORAGE_SECRET"],
    favicon="🍁",
    dark=False,
)