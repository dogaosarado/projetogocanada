# main.py

from nicegui import app, ui
from pages.landing import landing_page
from pages.login import login_page
from pages.form import form_page
from pages.confirmation import confirmation_page
from pages.admin import admin_page
from pages.interest import interest_page
import os
print(f"DEBUG API_URL: {os.getenv('API_URL', 'NAO DEFINIDO')}")

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


import os

ui.run(
    title="GoCanada",
    port=int(os.getenv("PORT", 8080)),
    storage_secret="gocanada-secret-key-troca-isso",
    favicon="🍁",
    dark=False,
    host="0.0.0.0",
)