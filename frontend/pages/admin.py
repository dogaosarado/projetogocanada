# pages/admin.py

from nicegui import ui
from state.user import get_token, get_is_admin, is_logged_in  # get_is_admin: NOVO, ver aviso no chat
import httpx
import os
from dotenv import load_dotenv
from frontend.services.api import delete_user, send_payment_link
from state.user import logout
from pages.layout import authenticated_header
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.user import User

load_dotenv()
API_URL = os.getenv("API_URL", "http://localhost:8000")

# Rótulos e agrupamento pra exibir os dois produtos sem confundir o admin
REPORT_TIER_OPTIONS = {
    "relatorio_gratis": "Relatório — Grátis",
    "relatorio_basico": "Relatório — Básico",
    "relatorio_intermediario": "Relatório — Intermediário",
    "relatorio_avancado": "Relatório — Avançado",
}
MENTORSHIP_TIER_OPTIONS = {
    "mentoria_basico": "Mentoria — Básico",
    "mentoria_intermediario": "Mentoria — Intermediário",
    "mentoria_avancado": "Mentoria — Avançado",
}
ALL_TIER_OPTIONS = {**REPORT_TIER_OPTIONS, **MENTORSHIP_TIER_OPTIONS}


def get_users(db: Session) -> list:
    return db.query(User).order_by(User.created_at.desc()).all()

def create_user(token: str, email: str, password: str, tier: str) -> dict | None:
    try:
        response = httpx.post(
            f"{API_URL}/admin/users",
            json={"email": email, "password": password, "tier": tier},
            headers={"Authorization": f"bearer {token}"},
        )
        if response.status_code == 201:
            return response.json()
        return None
    except Exception:
        return None


def activate_user(token: str, user_id: int, tier: str) -> dict | None:
    try:
        response = httpx.patch(
            f"{API_URL}/admin/users/{user_id}/tier",
            json={"tier": tier},
            headers={"Authorization": f"bearer {token}"},
        )
        if response.status_code == 200:
            return response.json()
        return None
    except Exception:
        return None

def admin_page(db: Session = Depends(get_db)):
    db = SessionLocal()
    try:
        users = get_users(db)
        if not is_logged_in():
            ui.navigate.to("/login")
            return

        token = get_token()

        # ANTES: `if tier != "avancado": ui.navigate.to("/")`. Isso quebra
        # sozinho com o rename do enum, e já era furado antes disso — qualquer
        # cliente pagante do plano avançado do relatório caía direto no painel
        # admin. Troquei pra um campo explícito. Ver aviso no chat: isso só
        # funciona se state/user.py expuser get_is_admin() lendo o campo
        # is_admin que agora vem em UserResponse/auth/me.
        if not get_is_admin():
            ui.navigate.to("/")
            return

        users = get_users(token)

        with ui.column().classes("w-full min-h-screen bg-stone-50 items-center py-12 px-4"):
            authenticated_header()
            with ui.card().classes("w-full max-w-4xl p-8 shadow-lg rounded-2xl bg-white"):
                with ui.row().classes("w-full justify-between items-center mb-6"):
                    ui.label("Painel Admin").classes("text-2xl font-bold text-amber-700")
                    ui.button("Voltar", on_click=lambda: ui.navigate.to("/")).classes(
                        "bg-stone-200 text-stone-700 rounded-xl px-4 py-2"
                    )
                    ui.button("Gerenciar Blog", on_click=lambda: ui.navigate.to("/admin/blog")).classes(
                        "bg-amber-600 text-white rounded-xl px-4 py-2 hover:bg-amber-700"
                    )
                    add_logout_button()

                # criar usuário
                ui.label("Novo cliente").classes("text-lg font-semibold text-stone-700 mb-2")
                with ui.row().classes("w-full gap-3 items-end flex-wrap"):
                    new_email = ui.input("Email").classes("flex-1")
                    new_password = ui.input("Senha", password=True).classes("flex-1")
                    new_tier = ui.select(
                        ALL_TIER_OPTIONS,
                        label="Plano",
                        value="relatorio_basico",
                    ).classes("w-56")
                    create_msg = ui.label("").classes("text-sm")
                    create_msg.set_visibility(False)

                    def handle_create():
                        result = create_user(token, new_email.value, new_password.value, new_tier.value)
                        if result:
                            create_msg.text = f"Usuário {result['email']} criado."
                            create_msg.classes("text-green-600")
                            create_msg.set_visibility(True)
                            new_email.value = ""
                            new_password.value = ""
                            ui.navigate.to("/admin")
                        else:
                            create_msg.text = "Erro ao criar usuário."
                            create_msg.classes("text-red-500")
                            create_msg.set_visibility(True)

                    ui.button("Criar", on_click=handle_create).classes(
                        "bg-amber-600 text-white rounded-xl px-5 py-2 hover:bg-amber-700"
                    )

                ui.separator().classes("my-6")

                # lista de usuários
                ui.label("Clientes").classes("text-lg font-semibold text-stone-700 mb-4")

                if not users:
                    ui.label("Nenhum cliente cadastrado.").classes("text-stone-400")
                else:
                    with ui.column().classes("w-full gap-3"):
                        for user in users:
                            with ui.card().classes("w-full p-4 bg-stone-50 rounded-xl"):
                                with ui.row().classes("w-full justify-between items-center flex-wrap gap-3"):
                                    with ui.column().classes("gap-1"):
                                        ui.label(user["email"]).classes("font-medium text-stone-800")
                                        status = "Pago" if user["is_active"] else "Pendente"
                                        status_color = "text-green-600" if user["is_active"] else "text-red-500"
                                        tier_label = ALL_TIER_OPTIONS.get(user["tier"], user["tier"])
                                        ui.label(f"{tier_label} — {status}").classes(
                                            f"text-sm {status_color}"
                                        )

                                    with ui.row().classes("gap-2 items-center"):
                                        tier_select = ui.select(
                                            ALL_TIER_OPTIONS,
                                            value=user["tier"],
                                        ).classes("w-56")
                                        activate_msg = ui.label("").classes("text-sm text-green-600")
                                        activate_msg.set_visibility(False)

                                        def handle_activate(uid=user["id"], ts=tier_select, msg=activate_msg):
                                            result = activate_user(token, uid, ts.value)
                                            if result:
                                                msg.text = "Pagamento confirmado."
                                                msg.set_visibility(True)
                                            else:
                                                msg.text = "Erro."
                                                msg.set_visibility(True)
                                        async def handle_delete(uid=user["id"]):
                                            result = await delete_user(token, uid)
                                            if result:
                                                ui.navigate.to("/admin")
                                            else:
                                                ui.notify("Erro ao deletar.", color="negative")

                                        ui.button("Deletar", on_click=handle_delete).classes(
                                            "bg-red-500 text-white rounded-xl px-4 py-2 hover:bg-red-600"
                                        )
                                        ui.button("Confirmar pagamento", on_click=handle_activate).classes(
                                            "bg-amber-600 text-white rounded-xl px-4 py-2 hover:bg-amber-700"
                                        )
                                        ui.button("Ver detalhes", on_click=lambda uid=user["id"]: ui.navigate.to(f"/admin/users/{uid}")).classes(
        "bg-stone-600 text-white rounded-xl px-4 py-2 hover:bg-stone-700"
    )

                                with ui.row().classes("w-full gap-2 items-center mt-2"):
                                    pix_input = ui.input("Link do Pix").classes("flex-1")
                                    pix_msg = ui.label("").classes("text-sm")
                                    pix_msg.set_visibility(False)

                                    async def handle_send_pix(uid=user["id"], link=pix_input, msg=pix_msg):
                                        if not link.value:
                                            msg.text = "Cole o link antes de enviar."
                                            msg.classes(replace="text-sm text-red-500")
                                            msg.set_visibility(True)
                                            return
                                        ok = await send_payment_link(token, uid, link.value)
                                        if ok:
                                            msg.text = "Cobrança enviada."
                                            msg.classes(replace="text-sm text-green-600")
                                            link.value = ""
                                        else:
                                            msg.text = "Erro ao enviar."
                                            msg.classes(replace="text-sm text-red-500")
                                        msg.set_visibility(True)

                                    ui.button("Enviar cobrança", on_click=handle_send_pix).classes(
                                        "bg-amber-600 text-white rounded-xl px-4 py-2 hover:bg-amber-700"
                                    )
    finally:
        db.close()
def add_logout_button():
    ui.button('Logoff', on_click=lambda: (logout(), ui.navigate.to('/login'))).props('flat color=negative')
