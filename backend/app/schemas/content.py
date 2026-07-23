from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional


class PostCreate(BaseModel):
    title: str
    slug: str
    body_html: str
    published: bool = False

class PostUpdate(BaseModel):
    title: Optional[str] = None
    body_html: Optional[str] = None
    published: Optional[bool] = None

class PostResponse(BaseModel):
    id: int
    title: str
    slug: str
    body_html: str
    published: bool
    created_at: datetime
    class Config:
        from_attributes = True


class MeetingCreate(BaseModel):
    title: str
    scheduled_at: datetime
    notes: Optional[str] = None

class MeetingResponse(MeetingCreate):
    id: int
    class Config:
        from_attributes = True


class DeadlineCreate(BaseModel):
    label: str
    due_date: date

class DeadlineResponse(DeadlineCreate):
    id: int
    class Config:
        from_attributes = True


class ChecklistItemResponse(BaseModel):
    key: str
    label: str
    completed: bool


class DashboardResponse(BaseModel):
    name: Optional[str]
    tier: str
    meetings: list[MeetingResponse]
    deadlines: list[DeadlineResponse]
    checklist: list[ChecklistItemResponse]