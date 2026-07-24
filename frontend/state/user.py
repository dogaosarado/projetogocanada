# state/user.py

from nicegui import app


def set_user(token: str, email: str, tier: str, name: str | None = None, is_active: bool = False) -> None:
    app.storage.user["token"] = token
    app.storage.user["email"] = email
    app.storage.user["tier"] = tier
    app.storage.user["name"] = name
    app.storage.user["is_active"] = is_active

def get_name() -> str | None:
    return app.storage.user.get("name")

def get_token() -> str | None:
    return app.storage.user.get("token")

def get_tier() -> str | None:
    return app.storage.user.get("tier")

def get_email() -> str | None:
    return app.storage.user.get("email")

def is_logged_in() -> bool:
    return bool(app.storage.user.get("token"))

def get_is_active() -> bool:
    return bool(app.storage.user.get("is_active"))

def logout() -> None:
    app.storage.user.clear()