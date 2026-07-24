# services/api.py

import os
import httpx
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL", "http://localhost:8000")
print(f"API_URL carregado: {API_URL}")

API_URL = os.getenv("API_URL", "http://localhost:8000")

def get_me(token: str) -> dict | None:
    try:
        response = httpx.get(
            f"{API_URL}/auth/me",
            headers={"Authorization": f"bearer {token}"},
        )
        if response.status_code == 200:
            return response.json()
        return None
    except Exception:
        return None

def login(email: str, password: str) -> dict | None:
    try:
        response = httpx.post(
            f"{API_URL}/auth/login",
            json={"email": email, "password": password},
        )
        if response.status_code == 200:
            return response.json()
        return None
    except Exception:
        return None


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


def submit_request(token: str, payload: dict) -> dict | None:
    try:
        response = httpx.post(
            f"{API_URL}/requests",
            json=payload,
            headers={"Authorization": f"bearer {token}"},
        )
        if response.status_code == 201:
            return response.json()
        return None
    except Exception:
        return None

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


def toggle_checklist_item(token: str, item_key: str) -> dict | None:
    try:
        response = httpx.patch(
            f"{API_URL}/me/checklist/{item_key}",
            headers={"Authorization": f"bearer {token}"},
        )
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"toggle_checklist_item EXCEPTION: {type(e).__name__}: {e}")
        return None

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