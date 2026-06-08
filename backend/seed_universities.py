# seed_universities.py

import json
import sys
from app.core.database import SessionLocal
from app.models.university import University


def seed(json_path: str) -> None:
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    count = 0
    for entry in data:
        name = entry.get("name")
        programs = entry.get("programs", [])
        departments = [
            {"name": p["name"], "url": p.get("url")}
            for p in programs if p.get("name")
        ]

        if not name or not departments:
            print(f"Pulando entrada inválida: {name}")
            continue

        db = SessionLocal()
        try:
            exists = db.query(University).filter(University.name == name).first()
            if exists:
                print(f"Já existe: {name}")
                continue

            university = University(name=name, departments=departments)
            db.add(university)
            db.commit()
            print(f"OK: {name} — {len(departments)} departamentos")
            count += 1
        except Exception as e:
            db.rollback()
            print(f"ERRO em {name}: {e}")
        finally:
            db.close()

    print(f"\n{count} universidades inseridas.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python seed_universities.py caminho/para/universities.json")
        sys.exit(1)
    seed(sys.argv[1])