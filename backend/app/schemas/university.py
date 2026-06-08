# app/schemas/university.py

from pydantic import BaseModel


class DepartmentSchema(BaseModel):
    name: str
    url: str | None = None


class UniversityResponse(BaseModel):
    id: int
    name: str
    departments: list[DepartmentSchema]

    model_config = {"from_attributes": True}