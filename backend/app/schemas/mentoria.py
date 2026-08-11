# app/schemas/mentoria.py

from pydantic import BaseModel, EmailStr, field_validator

from app.models.user import TierEnum
from app.schemas.request import UniversitySelection

MENTORSHIP_TIERS = {
    TierEnum.mentoria_basico,
    TierEnum.mentoria_intermediario,
    TierEnum.mentoria_avancado,
}

# ASSUNÇÃO: doc não definia limite de universidades por tier de mentoria
# (os tiers de lá são sobre nº de encontros, não universidades). Espelhando
# a progressão do relatório por posição. Troca aqui se quiser outro número.
MENTORSHIP_UNIVERSITY_LIMITS = {
    TierEnum.mentoria_basico: 2,
    TierEnum.mentoria_intermediario: 3,
    TierEnum.mentoria_avancado: 4,
}


class MentoriaSignupCreate(BaseModel):
    name: str
    email: EmailStr
    tier: TierEnum
    universities_selected: list[UniversitySelection]
    research_interests: str | None = None  # campo do lattes, opcional

    @field_validator("tier")
    @classmethod
    def tier_must_be_mentorship(cls, v: TierEnum):
        if v not in MENTORSHIP_TIERS:
            raise ValueError("Tier inválido para cadastro de mentoria.")
        return v

    @field_validator("universities_selected")
    @classmethod
    def at_least_one_university(cls, v: list[UniversitySelection]):
        if not v:
            raise ValueError("Selecione ao menos uma universidade.")
        return v

    def validate_against_tier(self) -> None:
        limit = MENTORSHIP_UNIVERSITY_LIMITS[self.tier]
        if len(self.universities_selected) > limit:
            raise ValueError(f"Seu plano permite no máximo {limit} universidade(s).")

class MentoriaAddServiceCreate(BaseModel):
    tier: TierEnum
    universities_selected: list[UniversitySelection]
    research_interests: str | None = None

    @field_validator("tier")
    @classmethod
    def tier_must_be_mentorship(cls, v: TierEnum):
        if v not in MENTORSHIP_TIERS:
            raise ValueError("Tier inválido para cadastro de mentoria.")
        return v

    @field_validator("universities_selected")
    @classmethod
    def at_least_one_university(cls, v: list[UniversitySelection]):
        if not v:
            raise ValueError("Selecione ao menos uma universidade.")
        return v

    def validate_against_tier(self) -> None:
        limit = MENTORSHIP_UNIVERSITY_LIMITS[self.tier]
        if len(self.universities_selected) > limit:
            raise ValueError(f"Seu plano permite no máximo {limit} universidade(s).")