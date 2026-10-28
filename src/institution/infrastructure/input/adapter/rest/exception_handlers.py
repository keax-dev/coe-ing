# Tema: traducción de errores del dominio a respuestas HTTP.

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.institution.domain.exception.institution_errors import (
    InstitutionError,
    InstitutionNotFound,
    InstitutionPersistenceConflict,
    InstitutionPersistenceFailure,
    InstitutionVersionConflict,
    InvalidInstitution,
)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(InstitutionError)
    async def handle_institution_error(_request: Request, error: InstitutionError) -> JSONResponse:
        statuses = {
            InvalidInstitution: (422, "INVALID_INSTITUTION"),
            InstitutionNotFound: (404, "INSTITUTION_NOT_FOUND"),
            InstitutionVersionConflict: (409, "VERSION_CONFLICT"),
            InstitutionPersistenceConflict: (409, "PERSISTENCE_CONFLICT"),
            InstitutionPersistenceFailure: (503, "PERSISTENCE_UNAVAILABLE"),
        }
        status_code, code = statuses.get(type(error), (500, "INTERNAL_ERROR"))
        # Los adaptadores ya ocultan detalles SQL y credenciales en los mensajes públicos.
        return JSONResponse(status_code=status_code, content={"code": code, "message": str(error)})
