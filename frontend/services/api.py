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
        )
        if response.status_code == 201:
            return response.json()
        return None
    except Exception:
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