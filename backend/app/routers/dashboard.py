from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.deps import get_db, get_current_user
from app.models.content import Meeting, Deadline, ChecklistProgress
from app.models.request import Application
from app.models.user import User
from app.schemas.content import DashboardResponse, ApplicationSummary, ApplicationDetailResponse, ChecklistItemResponse
from app.core.checklist_items import CHECKLIST_ITEMS

router = APIRouter(prefix="/me", tags=["dashboard"])


def _get_owned_application(application_id: int, user: User, db: Session) -> Application:
    application = db.query(Application).filter(
        Application.id == application_id, Application.user_id == user.id
    ).first()
    if application is None:
        raise HTTPException(404, "Candidatura não encontrada.")
    return application


@router.get("/dashboard", response_model=DashboardResponse)
def get_dashboard(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if not user.is_active:
        raise HTTPException(403, "Conta ainda não ativada.")

    meetings = db.query(Meeting).filter(Meeting.user_id == user.id).order_by(Meeting.scheduled_at).all()
    applications = db.query(Application).filter(Application.user_id == user.id).order_by(Application.created_at).all()

    total_items = len(CHECKLIST_ITEMS)
    summaries = []
    for app_ in applications:
        deadline_count = db.query(Deadline).filter(Deadline.application_id == app_.id).count()
        checklist_done = db.query(ChecklistProgress).filter(
            ChecklistProgress.application_id == app_.id, ChecklistProgress.completed == True
        ).count()
        summaries.append(ApplicationSummary(
            id=app_.id,
            university=app_.university,
            department=app_.department,
            url=app_.url,
            is_custom=app_.is_custom,
            deadline_count=deadline_count,
            checklist_done=checklist_done,
            checklist_total=total_items,
        ))

    return {
        "name": user.name,
        "tier": user.tier.value,
        "meetings": meetings,
        "applications": summaries,
    }


@router.get("/applications/{application_id}", response_model=ApplicationDetailResponse)
def get_application_detail(application_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if not user.is_active:
        raise HTTPException(403, "Conta ainda não ativada.")

    application = _get_owned_application(application_id, user, db)

    deadlines = db.query(Deadline).filter(Deadline.application_id == application.id).order_by(Deadline.due_date).all()
    progress = {
        p.item_key: p.completed
        for p in db.query(ChecklistProgress).filter(ChecklistProgress.application_id == application.id).all()
    }
    checklist = [
        ChecklistItemResponse(key=item["key"], label=item["label"], completed=progress.get(item["key"], False))
        for item in CHECKLIST_ITEMS
    ]

    return ApplicationDetailResponse(
        id=application.id,
        university=application.university,
        department=application.department,
        url=application.url,
        is_custom=application.is_custom,
        deadlines=deadlines,
        checklist=checklist,
    )


@router.patch("/applications/{application_id}/checklist/{item_key}")
def toggle_application_checklist_item(
    application_id: int, item_key: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    if not user.is_active:
        raise HTTPException(403, "Conta ainda não ativada.")

    application = _get_owned_application(application_id, user, db)

    valid_keys = {i["key"] for i in CHECKLIST_ITEMS}
    if item_key not in valid_keys:
        raise HTTPException(404, "Item inválido.")

    entry = db.query(ChecklistProgress).filter(
        ChecklistProgress.application_id == application.id, ChecklistProgress.item_key == item_key
    ).first()

    if entry:
        entry.completed = not entry.completed
    else:
        entry = ChecklistProgress(
            user_id=user.id, application_id=application.id, item_key=item_key, completed=True
        )
        db.add(entry)

    db.commit()
    return {"key": item_key, "completed": entry.completed}
