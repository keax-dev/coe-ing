# Tema: rutas REST que delegan el CRUD al servicio de aplicación.

from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, Response

from src.education.clean.application.service.education_service import EducationService
from src.education.clean.presentation.dependency.education_dependencies import get_education_service
from src.education.clean.presentation.mapper.education_rest_mapper import EducationRestMapper
from src.education.clean.presentation.schema.education_schema import (
    EducationCreateRequest,
    EducationResponse,
    EducationUpdateRequest,
)

router = APIRouter(prefix="/api/v1/educations", tags=["Educations"])
Service = Annotated[EducationService, Depends(get_education_service)]
EducationId = Annotated[int, Path(gt=0)]


@router.post("", status_code=201, response_model=EducationResponse)
def create_education(
    request: EducationCreateRequest, service: Service, response: Response
) -> EducationResponse:
    education = service.create(EducationRestMapper.from_create(request))
    response.headers["Location"] = f"/api/v1/educations/{education.education_id}"
    return EducationRestMapper.to_response(education)


@router.get("", response_model=list[EducationResponse])
def list_educations(
    service: Service,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    institution_id: Annotated[int | None, Query(alias="institutionId", gt=0)] = None,
    visible: Annotated[bool | None, Query()] = None,
) -> list[EducationResponse]:
    return [
        EducationRestMapper.to_response(education)
        for education in service.list(offset, limit, institution_id, visible)
    ]


@router.get("/{education_id}", response_model=EducationResponse)
def get_education(education_id: EducationId, service: Service) -> EducationResponse:
    return EducationRestMapper.to_response(service.get(education_id))


@router.put("/{education_id}", response_model=EducationResponse)
def update_education(
    education_id: EducationId, request: EducationUpdateRequest, service: Service
) -> EducationResponse:
    return EducationRestMapper.to_response(
        service.update(EducationRestMapper.from_update(education_id, request))
    )


@router.delete("/{education_id}", status_code=204)
def delete_education(
    education_id: EducationId, version: Annotated[int, Query(ge=0)], service: Service
) -> Response:
    service.delete(education_id, version)
    return Response(status_code=204)
