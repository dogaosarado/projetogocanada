from pydantic import BaseModel, field_validator

from app.models.user import TierEnum


TIER_LIMITS = {
    TierEnum.relatorio_gratis:        {"universities": 1},
    TierEnum.relatorio_basico:        {"universities": 2},
    TierEnum.relatorio_intermediario: {"universities": 3},
    TierEnum.relatorio_avancado:      {"universities": 4},
}


class UniversitySelection(BaseModel):
    university: str
    department: str
    url: str | None = None
    is_custom: bool = False


class RequestCreate(BaseModel):
    universities_selected: list[UniversitySelection]
    research_interests: str | None = None

    @field_validator("universities_selected")
    @classmethod
    def at_least_one_university(cls, v: list[UniversitySelection]):
        if not v:
            raise ValueError("Selecione ao menos uma universidade.")
        return v

    def validate_against_tier(self, tier: TierEnum) -> None:
        limits = TIER_LIMITS.get(tier)
        if limits is None:
            # planos de mentoria (mentoria_*) não têm formulário de
            # universidades — se isso disparar, é o endpoint errado sendo
            # chamado pro tier errado, não um tier novo que falta cadastrar.
            raise ValueError(
                "Este plano não usa seleção de universidades."
            )
        if len(self.universities_selected) > limits["universities"]:
            raise ValueError(
                f"Seu plano permite no máximo {limits['universities']} universidade(s)."
            )


class RequestResponse(BaseModel):
    id: int
    tier: str
    universities_selected: list[UniversitySelection]
    research_interests: str | None

    model_config = {"from_attributes": True}


class ApplicationResponse(BaseModel):
    id: int
    university: str
    department: str
    url: str | None = None
    is_custom: bool

    model_config = {"from_attributes": True}