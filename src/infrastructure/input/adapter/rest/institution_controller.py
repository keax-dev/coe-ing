# Tema: adaptador REST que depende únicamente del puerto de entrada.

from typing import Annotated, cast

from fastapi import APIRouter, Depends, Path, Query, Request, Response, status

from src.application.port.input.institution_service import InstitutionService
from src.infrastructure.input.adapter.rest.dto.institution_dto import (
    InstitutionCreateRequest,
    InstitutionResponse,
    InstitutionUpdateRequest,
)
from src.infrastructure.input.adapter.rest.mapper.institution_rest_mapper import (
    InstitutionRestMapper,
)

router = APIRouter(prefix="/api/v1/institutions", tags=["Institutions"])


def get_institution_service(request: Request) -> InstitutionService:
    # La configuración ensambla las dependencias; el controlador solo recibe el contrato.
    return cast(InstitutionService, request.app.state.institution_service)


Service = Annotated[InstitutionService, Depends(get_institution_service)]
InstitutionId = Annotated[int, Path(gt=0)]


@router.post("", response_model=InstitutionResponse, status_code=status.HTTP_201_CREATED)
def create_institution(
    request: InstitutionCreateRequest, service: Service, response: Response
) -> InstitutionResponse:
    institution = service.create(InstitutionRestMapper.from_create(request))
    response.headers["Location"] = f"/api/v1/institutions/{institution.institution_id}"
    return InstitutionRestMapper.to_response(institution)


@router.get("", response_model=list[InstitutionResponse])
def list_institutions(
    service: Service,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
) -> list[InstitutionResponse]:
    return [
        InstitutionRestMapper.to_response(institution)
        for institution in service.list(offset, limit)
    ]


@router.get("/{institution_id}", response_model=InstitutionResponse)
def get_institution(institution_id: InstitutionId, service: Service) -> InstitutionResponse:
    return InstitutionRestMapper.to_response(service.get(institution_id))


@router.put("/{institution_id}", response_model=InstitutionResponse)
def update_institution(
    institution_id: InstitutionId, request: InstitutionUpdateRequest, service: Service
) -> InstitutionResponse:
    institution = service.update(InstitutionRestMapper.from_update(institution_id, request))
    return InstitutionRestMapper.to_response(institution)


@router.delete("/{institution_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_institution(
    institution_id: InstitutionId, version: Annotated[int, Query(ge=0)], service: Service
) -> Response:
    service.delete(institution_id, version)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
