# main.py

from nicegui import app, ui
from pages.landing import landing_page
from pages.login import login_page
from pages.form import form_page
from pages.confirmation import confirmation_page
from pages.admin import admin_page

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


ui.run(
    title="GoCanada",
    port=8080,
    storage_secret="gocanada-secret-key-troca-isso",
    favicon="🍁",
    dark=False,
)