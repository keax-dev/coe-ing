# Tema: traducción entre esquemas HTTP y entidades de dominio.

from dataclasses import asdict

from src.education.clean.domain.model.education import Education
from src.education.clean.presentation.schema.education_schema import (
    EducationCreateRequest,
    EducationResponse,
    EducationUpdateRequest,
)


class EducationRestMapper:
    @staticmethod
    def from_create(request: EducationCreateRequest) -> Education:
        return Education(**request.model_dump())

    @staticmethod
    def from_update(education_id: int, request: EducationUpdateRequest) -> Education:
        return Education(education_id=education_id, **request.model_dump())

    @staticmethod
    def to_response(education: Education) -> EducationResponse:
        return EducationResponse(**asdict(education))
