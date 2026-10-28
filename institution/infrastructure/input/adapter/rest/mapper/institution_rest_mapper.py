# Tema: conversiones explícitas entre DTO HTTP y modelos de dominio.

from institution.domain.model.institution import Institution
from institution.infrastructure.input.adapter.rest.dto.institution_dto import (
    InstitutionCreateRequest,
    InstitutionResponse,
    InstitutionUpdateRequest,
)


class InstitutionRestMapper:
    @staticmethod
    def from_create(request: InstitutionCreateRequest) -> Institution:
        return Institution(**request.model_dump())

    @staticmethod
    def from_update(institution_id: int, request: InstitutionUpdateRequest) -> Institution:
        return Institution(institution_id=institution_id, **request.model_dump())

    @staticmethod
    def to_response(institution: Institution) -> InstitutionResponse:
        return InstitutionResponse(
            institution_id=institution.institution_id,
            institution_name=institution.institution_name,
            institution_name_es=institution.institution_name_es,
            institution_url=institution.institution_url,
            institution_deleted=institution.institution_deleted,
            version=institution.version,
        )
