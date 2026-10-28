# Tema: contratos HTTP validados sin exponer las entidades de persistencia.

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class InstitutionFields(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel, populate_by_name=True, extra="forbid", str_strip_whitespace=True
    )

    institution_name: str = Field(min_length=1, max_length=255)
    institution_name_es: str | None = Field(default=None, max_length=255)
    institution_url: str | None = Field(default=None, max_length=2048)


class InstitutionCreateRequest(InstitutionFields):
    pass


class InstitutionUpdateRequest(InstitutionFields):
    version: int = Field(ge=0, strict=True)


class InstitutionResponse(InstitutionFields):
    institution_id: int
    institution_deleted: bool
    version: int
