# Tema: ensamblado externo e inyección del servicio de educación.

from typing import cast

from fastapi import Request
from sqlalchemy.orm import Session, sessionmaker

from src.education.clean.application.service.education_service import EducationService
from src.education.clean.infrastructure.unit_of_work.sqlalchemy_unit_of_work import (
    SQLAlchemyUnitOfWork,
)


def configure_education_service(session_factory: sessionmaker[Session]) -> EducationService:
    # Cada invocación del servicio obtiene una unidad de trabajo y una sesión nuevas.
    return EducationService(lambda: SQLAlchemyUnitOfWork(session_factory))


def get_education_service(request: Request) -> EducationService:
    return cast(EducationService, request.app.state.education_service)
