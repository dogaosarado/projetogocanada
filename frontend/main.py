# main.py

from nicegui import app, ui
from pages.relatorio import relatorio_page
from pages.mentoria import mentoria_page
from pages.contact import contact_page
from pages.login import login_page
from pages.form import form_page
from pages.confirmation import confirmation_page
from pages.admin import admin_page
from pages.admin_relatorio import admin_relatorio_page
from pages.interest import interest_page
from pages.dashboard import dashboard_page
from pages.blog import blog_list_page, blog_post_page
from pages.admin_client import admin_client_page
from pages.admin_blog import admin_blog_page
from pages.application_detail import application_detail_page
from pages.about import about_page
from pages.mentoria_signup import mentoria_signup_page
from pages.relatorio_signup import relatorio_signup_page
from pages.relatorio_interest import relatorio_interest_page
from pages.change_password_forced import change_password_forced_page
from pages.mentoria_interest import mentoria_interest_page
from pages.mentoria_adicionar import mentoria_adicionar_page
from pages.relatorio_adicionar import relatorio_adicionar_page
import os

print(f"DEBUG API_URL: {os.getenv('API_URL', 'NAO DEFINIDO')}")

app.add_static_files("/assets", os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets"))

ui.add_head_html('''
<title>GoCanadaBR</title>
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

@ui.page("/interesse", title="GoCanadaBR")
def interesse():
    interest_page()

@ui.page("/admin", title="GoCanadaBR")
def admin():
    admin_page()

@ui.page("/admin/relatorio", title="GoCanadaBR")
def admin_relatorio():
    admin_relatorio_page()

@ui.page("/", title="GoCanadaBR")
def index():
    mentoria_page()


@ui.page("/relatorio", title="GoCanadaBR")
def relatorio():
    relatorio_page()


@ui.page("/contato", title="GoCanadaBR")
def contato():
    contact_page()


@ui.page("/mentoria", title="GoCanadaBR")
def mentoria_redirect():
    # rota antiga — mantida só pra não quebrar link/bookmark/SEO já existente
    ui.navigate.to("/")


@ui.page("/login", title="GoCanadaBR")
def login():
    login_page()


@ui.page("/formulario", title="GoCanadaBR")
def formulario():
    form_page()


@ui.page("/confirmacao", title="GoCanadaBR")
def confirmacao():
    confirmation_page()

@ui.page("/painel", title="GoCanadaBR")
def painel():
    dashboard_page()

@ui.page("/blog", title="GoCanadaBR")
def blog():
    blog_list_page()

@ui.page("/blog/{slug}", title="GoCanadaBR")
def blog_post(slug: str):
    blog_post_page(slug)

@ui.page("/admin/users/{user_id}", title="GoCanadaBR")
def admin_client(user_id: int):
    admin_client_page(user_id)

@ui.page("/admin/blog", title="GoCanadaBR")
def admin_blog():
    admin_blog_page()

@ui.page("/painel/candidatura/{application_id}", title="GoCanadaBR")
def painel_candidatura(application_id: int):
    application_detail_page(application_id)

@ui.page("/quem-somos", title="GoCanadaBR")
def quem_somos():
    about_page()

@ui.page("/mentoria/interesse", title="GoCanadaBR")
def mentoria_interesse():
    mentoria_interest_page()

@ui.page("/mentoria/cadastro", title="GoCanadaBR")
def mentoria_cadastro(tier: str = "mentoria_basico"):
    mentoria_signup_page(tier)

@ui.page("/relatorio/interesse", title="GoCanadaBR")
def relatorio_interesse():
    relatorio_interest_page()

@ui.page("/relatorio/cadastro", title="GoCanadaBR")
def relatorio_cadastro(tier: str = "relatorio_gratis"):
    relatorio_signup_page(tier)

@ui.page("/trocar-senha", title="GoCanadaBR")
def trocar_senha():
    change_password_forced_page()

@ui.page("/relatorio/adicionar", title="GoCanadaBR")
def relatorio_adicionar(tier: str = "relatorio_gratis"):
    relatorio_adicionar_page(tier)

@ui.page("/mentoria/adicionar", title="GoCanadaBR")
def mentoria_adicionar(tier: str = "mentoria_basico"):
    mentoria_adicionar_page(tier)

ui.run(
    title="GoCanadaBR",
    port=int(os.getenv("PORT", 8081)),
    storage_secret=os.environ["STORAGE_SECRET"],
    favicon="🍁",
    dark=False,
    host="0.0.0.0",
)
