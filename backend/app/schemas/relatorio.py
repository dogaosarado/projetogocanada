# app/schemas/relatorio.py

from pydantic import BaseModel, EmailStr, field_validator

from app.models.user import TierEnum
from app.schemas.request import UniversitySelection

REPORT_TIERS = {
    TierEnum.relatorio_gratis,
    TierEnum.relatorio_basico,
    TierEnum.relatorio_intermediario,
    TierEnum.relatorio_avancado,
}

# Mesmos números que já estavam duplicados em app/routers/relatorio.py
# e em pages/relatorio_signup.py. Centralizado aqui.
REPORT_UNIVERSITY_LIMITS = {
    TierEnum.relatorio_gratis: 1,
    TierEnum.relatorio_basico: 2,
    TierEnum.relatorio_intermediario: 3,
    TierEnum.relatorio_avancado: 4,
}

class RelatorioAddServiceCreate(BaseModel):
    tier: TierEnum
    universities_selected: list[UniversitySelection]
    lattes_url: str | None = None

    @field_validator("tier")
    @classmethod
    def tier_must_be_relatorio(cls, v: TierEnum):
        if v not in REPORT_TIERS:
            raise ValueError("Tier inválido para cadastro de relatório.")
        return v

    @field_validator("universities_selected")
    @classmethod
    def at_least_one_university(cls, v: list[UniversitySelection]):
        if not v:
            raise ValueError("Selecione ao menos uma universidade.")
        return v

    def validate_against_tier(self) -> None:
        limit = REPORT_UNIVERSITY_LIMITS[self.tier]
        if len(self.universities_selected) > limit:
            raise ValueError(f"Seu plano permite no máximo {limit} universidade(s).")

class RelatorioSignupCreate(BaseModel):
    name: str
    email: EmailStr
    tier: TierEnum
    universities_selected: list[UniversitySelection]
    lattes_url: str | None = None

    @field_validator("tier")
    @classmethod
    def tier_must_be_relatorio(cls, v: TierEnum):
        if v not in REPORT_TIERS:
            raise ValueError("Tier inválido para cadastro de relatório.")
        return v

    @field_validator("universities_selected")
    @classmethod
    def at_least_one_university(cls, v: list[UniversitySelection]):
        if not v:
            raise ValueError("Selecione ao menos uma universidade.")
        return v

    def validate_against_tier(self) -> None:
        limit = REPORT_UNIVERSITY_LIMITS[self.tier]
        if len(self.universities_selected) > limit:
            raise ValueError(f"Seu plano permite no máximo {limit} universidade(s).")