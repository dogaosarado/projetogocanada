# clean_universities.py

from app.core.database import SessionLocal
from app.models.university import University

JUNK_KEYWORDS = [
    "privacy", "contact", "login", "logout", "sign in", "sign up",
    "accessibility", "terms", "copyright", "feedback", "sitemap",
    "site map", "webmail", "directory", "donate", "careers", "alumni",
    "library", "libraries", "campus", "international", "map", "search",
    "menu", "navigation", "home", "about", "news", "events", "apply",
    "admission", "tuition", "scholarship", "award", "funding", "faq",
    "policy", "policies", "emergency", "security", "cookie", "gdpr",
    "last updated", "copyright @", "powered by", "zoom", "hybrid",
    "virtual tour", "give to", "phone directory", "web standards",
    "web feedback", "a-z", "az index", "switch to", "download page",
    "faculty + staff", "faculty and staff", "current students",
    "future students", "postdoc", "dean's", "graduate studies",
    "click here", "learn more", "read more", "see more", "view all",
    "back to", "return to", "skip to", "jump to",
]


def is_junk(name: str) -> bool:
    lower = name.lower()
    if len(name) < 4:
        return True
    if any(keyword in lower for keyword in JUNK_KEYWORDS):
        return True
    return False


def clean():
    db = SessionLocal()
    universities = db.query(University).all()

    total_removed = 0
    for university in universities:
        original = university.departments
        cleaned = [d for d in original if not is_junk(d)]
        removed = len(original) - len(cleaned)

        if removed > 0:
            print(f"{university.name}: {len(original)} → {len(cleaned)} ({removed} removidos)")
            university.departments = cleaned
            total_removed += removed

    db.commit()
    db.close()
    print(f"\nTotal removido: {total_removed} entradas")


if __name__ == "__main__":
    clean()