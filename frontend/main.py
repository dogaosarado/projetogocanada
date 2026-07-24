# main.py

from nicegui import app, ui
from pages.landing import landing_page
from pages.login import login_page
from pages.form import form_page
from pages.confirmation import confirmation_page
from pages.admin import admin_page
from pages.interest import interest_page
from pages.dashboard import dashboard_page
from pages.blog import blog_list_page, blog_post_page
import os

print(f"DEBUG API_URL: {os.getenv('API_URL', 'NAO DEFINIDO')}")

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

@ui.page("/interesse")
def interesse():
    interest_page()

@ui.page("/admin")
def admin():
    admin_page()

@ui.page("/")
def index():
    landing_page()


@ui.page("/login")
def login():
    login_page()


@ui.page("/formulario")
def formulario():
    form_page()


@ui.page("/confirmacao")
def confirmacao():
    confirmation_page()

@ui.page("/painel")
def painel():
    dashboard_page()

@ui.page("/blog")
def blog():
    blog_list_page()

@ui.page("/blog/{slug}")
def blog_post(slug: str):
    blog_post_page(slug)

ui.run(
    title="GoCanada",
    port=int(os.getenv("PORT", 8080)),
    storage_secret=os.environ["STORAGE_SECRET"],
    favicon="🍁",
    dark=False,
    host="0.0.0.0",
)