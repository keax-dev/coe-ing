# Tema: traducción de errores de educación a respuestas HTTP sin detalles técnicos.

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.education.clean.domain.exception.education_errors import (
    ActiveInstitutionNotFound,
    EducationError,
    EducationNotFound,
    EducationPersistenceConflict,
    EducationPersistenceFailure,
    EducationVersionConflict,
    InvalidEducation,
)


def register_education_handlers(app: FastAPI) -> None:
    @app.exception_handler(EducationError)
    async def handle_error(_request: Request, error: EducationError) -> JSONResponse:
        codes = {
            InvalidEducation: (422, "INVALID_EDUCATION"),
            EducationNotFound: (404, "EDUCATION_NOT_FOUND"),
            ActiveInstitutionNotFound: (404, "ACTIVE_INSTITUTION_NOT_FOUND"),
            EducationVersionConflict: (409, "EDUCATION_VERSION_CONFLICT"),
            EducationPersistenceConflict: (409, "EDUCATION_PERSISTENCE_CONFLICT"),
            EducationPersistenceFailure: (503, "EDUCATION_PERSISTENCE_UNAVAILABLE"),
        }
        status, code = codes.get(type(error), (500, "INTERNAL_ERROR"))
        return JSONResponse(status_code=status, content={"code": code, "message": str(error)})
