# Tema: validación HTTP y serialización camelCase en el borde de FastAPI.

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class EducationFields(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel, populate_by_name=True, extra="forbid", str_strip_whitespace=True
    )

    education_title: str = Field(min_length=1, max_length=255)
    education_title_es: str | None = Field(default=None, max_length=255)
    education_place: str = Field(min_length=1, max_length=255)
    education_start: str | None = Field(default=None, max_length=255)
    education_start_es: str | None = Field(default=None, max_length=255)
    education_end: str = Field(min_length=1, max_length=255)
    education_end_es: str | None = Field(default=None, max_length=255)
    education_position: int = Field(ge=-(2**31), lt=2**31, strict=True)
    education_visible: bool = Field(default=True, strict=True)
    institution_id: int = Field(gt=0, strict=True)


class EducationCreateRequest(EducationFields):
    pass


class EducationUpdateRequest(EducationFields):
    version: int = Field(ge=0, strict=True)


class EducationResponse(EducationFields):
    education_id: int
    education_deleted: bool
    version: int
