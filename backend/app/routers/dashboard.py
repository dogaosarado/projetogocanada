from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.deps import get_db, get_current_user
from app.models.content import Meeting, Deadline, ChecklistProgress
from app.models.user import User
from app.schemas.content import DashboardResponse
from app.core.checklist_items import CHECKLIST_ITEMS

router = APIRouter(prefix="/me", tags=["dashboard"])

@router.get("/dashboard", response_model=DashboardResponse)
def get_dashboard(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
        if not user.is_active:
            raise HTTPException(403, "Conta ainda não ativada.")
        else:
            meetings = db.query(Meeting).filter(Meeting.user_id == user.id).order_by(Meeting.scheduled_at).all()
            deadlines = db.query(Deadline).filter(Deadline.user_id == user.id).order_by(Deadline.due_date).all()
            progress = {p.item_key: p.completed for p in db.query(ChecklistProgress).filter(ChecklistProgress.user_id == user.id).all()}

            checklist = [
                {"key": item["key"], "label": item["label"], "completed": progress.get(item["key"], False)}
                for item in CHECKLIST_ITEMS
            ]

        return {
            "name": user.name,
            "tier": user.tier.value,
            "meetings": meetings,
            "deadlines": deadlines,
            "checklist": checklist,
        }

@router.patch("/checklist/{item_key}")
def toggle_checklist_item(item_key: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if not user.is_active:
        raise HTTPException(403, "Conta ainda não ativada.")

    valid_keys = {i["key"] for i in CHECKLIST_ITEMS}
    if item_key not in valid_keys:
        raise HTTPException(404, "Item inválido.")

    entry = db.query(ChecklistProgress).filter(
        ChecklistProgress.user_id == user.id, ChecklistProgress.item_key == item_key
    ).first()

    if entry:
        entry.completed = not entry.completed
    else:
        entry = ChecklistProgress(user_id=user.id, item_key=item_key, completed=True)
        db.add(entry)

    db.commit()
    return {"key": item_key, "completed": entry.completed}