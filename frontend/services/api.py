# services/api.py

import os
import httpx
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL", "http://localhost:8000")
print(f"API_URL carregado: {API_URL}")

API_URL = os.getenv("API_URL", "http://localhost:8000")

def get_me(token: str) -> tuple[dict | None, str | None]:
    try:
        response = httpx.get(
            f"{API_URL}/auth/me",
            headers={"Authorization": f"bearer {token}"},
            timeout=30,
        )
        if response.status_code == 200:
            return response.json(), None
        return None, "Erro ao buscar dados do usuário."
    except Exception as e:
        print(f"get_me EXCEPTION: {type(e).__name__}: {e}")
        return None, "Erro de conexão. Tente novamente em instantes."

def login(email: str, password: str) -> dict | None:
    try:
        response = httpx.post(
            f"{API_URL}/auth/login",
            json={"email": email, "password": password},
            timeout=30,
        )
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"login EXCEPTION: {type(e).__name__}: {e}")
        return None

def get_universities_public() -> list | None:
    """Catálogo público, sem token — usado no cadastro de mentoria,
    antes de existir conta. Requer que /universities no backend não exija auth."""
    try:
        response = httpx.get(f"{API_URL}/universities")
        if response.status_code == 200:
            return response.json()
        return None
    except Exception:
        return None


def mentoria_signup(payload: dict) -> tuple[dict | None, str | None]:
    try:
        response = httpx.post(f"{API_URL}/mentoria/signup", json=payload, timeout=15)
        if response.status_code == 201:
            return response.json(), None
        try:
            detail = response.json().get("detail", "Erro ao cadastrar. Tente novamente.")
        except Exception:
            detail = "Erro ao cadastrar. Tente novamente."
        return None, detail
    except Exception:
        return None, "Erro de conexão. Tente novamente."

def get_universities(token: str) -> list | None:
    try:
        response = httpx.get(
            f"{API_URL}/universities",
            headers={"Authorization": f"bearer {token}"},
        )
        if response.status_code == 200:
            return response.json()
        return None
    except Exception:
        return None


def submit_request(token: str, payload: dict) -> tuple[dict | None, str | None]:
    try:
        response = httpx.post(
            f"{API_URL}/requests",
            json=payload,
            headers={"Authorization": f"bearer {token}"},
        )
        if response.status_code == 201:
            return response.json(), None
        try:
            detail = response.json().get("detail", "Erro ao enviar. Tente novamente.")
        except Exception:
            detail = "Erro ao enviar. Tente novamente."
        return None, detail
    except Exception:
        return None, "Erro de conexão. Tente novamente."


def get_request_status(token: str) -> bool:
    try:
        response = httpx.get(
            f"{API_URL}/requests/me/status",
            headers={"Authorization": f"bearer {token}"},
        )
        if response.status_code == 200:
            return response.json().get("has_submitted", False)
        return False
    except Exception:
        return False

def create_lead(name: str, email: str, tier: str) -> dict | None:
    try:
        response = httpx.post(
            f"{API_URL}/admin/leads",
            json={"name": name, "email": email, "tier": tier},
            timeout=15,
        )
        print(f"create_lead status={response.status_code} body={response.text}")
        if response.status_code == 201:
            return response.json()
        return None
    except Exception as e:
        print(f"create_lead EXCEPTION: {type(e).__name__}: {e}")
        return None

def delete_user(token: str, user_id: int) -> bool:
    try:
        response = httpx.delete(
            f"{API_URL}/admin/users/{user_id}",
            headers={"Authorization": f"bearer {token}"},
        )
        return response.status_code == 204
    except Exception:
        return False

def send_payment_link(token: str, user_id: int, pix_link: str) -> bool:
    try:
        response = httpx.post(
            f"{API_URL}/admin/users/{user_id}/send-payment-link",
            json={"pix_link": pix_link},
            headers={"Authorization": f"bearer {token}"},
        )
        return response.status_code == 200
    except Exception:
        return False


def get_dashboard(token: str) -> dict | None:
    try:
        response = httpx.get(
            f"{API_URL}/me/dashboard",
            headers={"Authorization": f"bearer {token}"},
        )
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"get_dashboard EXCEPTION: {type(e).__name__}: {e}")
        return None


def get_application_detail(token: str, application_id: int) -> dict | None:
    try:
        response = httpx.get(
            f"{API_URL}/me/applications/{application_id}",
            headers={"Authorization": f"bearer {token}"},
        )
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"get_application_detail EXCEPTION: {type(e).__name__}: {e}")
        return None


def toggle_application_checklist_item(token: str, application_id: int, item_key: str) -> dict | None:
    try:
        response = httpx.patch(
            f"{API_URL}/me/applications/{application_id}/checklist/{item_key}",
            headers={"Authorization": f"bearer {token}"},
        )
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"toggle_application_checklist_item EXCEPTION: {type(e).__name__}: {e}")
        return None


def change_password(token: str, current_password: str, new_password: str) -> tuple[bool, str]:
    try:
        response = httpx.post(
            f"{API_URL}/auth/change-password",
            json={"current_password": current_password, "new_password": new_password},
            headers={"Authorization": f"bearer {token}"},
        )
        if response.status_code == 200:
            return True, response.json().get("message", "Senha atualizada.")
        try:
            detail = response.json().get("detail", "Erro ao trocar senha.")
        except Exception:
            detail = "Erro ao trocar senha."
        return False, detail
    except Exception as e:
        print(f"change_password EXCEPTION: {type(e).__name__}: {e}")
        return False, "Erro de conexão."


def get_posts() -> list:
    try:
        response = httpx.get(f"{API_URL}/blog")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception:
        return []


def get_post(slug: str) -> dict | None:
    try:
        response = httpx.get(f"{API_URL}/blog/{slug}")
        if response.status_code == 200:
            return response.json()
        return None
    except Exception:
        return None


def get_all_posts_admin(token: str) -> list:
    try:
        response = httpx.get(
            f"{API_URL}/blog/admin/all",
            headers={"Authorization": f"bearer {token}"},
        )
        if response.status_code == 200:
            return response.json()
        return []
    except Exception:
        return []


def create_post_admin(token: str, title: str, slug: str, body_html: str, published: bool) -> dict | None:
    try:
        response = httpx.post(
            f"{API_URL}/blog/admin",
            json={"title": title, "slug": slug, "body_html": body_html, "published": published},
            headers={"Authorization": f"bearer {token}"},
        )
        if response.status_code == 201:
            return response.json()
        return None
    except Exception as e:
        print(f"create_post_admin EXCEPTION: {type(e).__name__}: {e}")
        return None


def update_post_admin(token: str, post_id: int, **fields) -> dict | None:
    try:
        response = httpx.patch(
            f"{API_URL}/blog/admin/{post_id}",
            json=fields,
            headers={"Authorization": f"bearer {token}"},
        )
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"update_post_admin EXCEPTION: {type(e).__name__}: {e}")
        return None


def delete_post_admin(token: str, post_id: int) -> bool:
    try:
        response = httpx.delete(
            f"{API_URL}/blog/admin/{post_id}",
            headers={"Authorization": f"bearer {token}"},
        )
        return response.status_code == 204
    except Exception:
        return False


def get_application_admin_detail(token: str, application_id: int) -> dict | None:
    try:
        response = httpx.get(
            f"{API_URL}/admin/applications/{application_id}/detail",
            headers={"Authorization": f"bearer {token}"},
        )
        if response.status_code == 200:
            return response.json()
        return None
    except Exception:
        return None


def add_deadline_to_application(token: str, application_id: int, label: str, due_date: str) -> dict | None:
    try:
        response = httpx.post(
            f"{API_URL}/admin/applications/{application_id}/deadlines",
            json={"label": label, "due_date": due_date},
            headers={"Authorization": f"bearer {token}"},
        )
        if response.status_code == 201:
            return response.json()
        return None
    except Exception:
        return None