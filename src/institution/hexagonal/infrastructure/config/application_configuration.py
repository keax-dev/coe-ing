# Tema: ensamblado de puertos, servicios y adaptadores por inyección de constructor.

from sqlalchemy.orm import Session, sessionmaker

from src.institution.hexagonal.application.port.input.institution_service import InstitutionService
from src.institution.hexagonal.application.service.institution_service_impl import (
    InstitutionServiceImpl,
)
from src.institution.hexagonal.infrastructure.output.adapter.repository.institution_persistence_adapter import (
    InstitutionPersistenceAdapter,
)


def configure_institution_service(session_factory: sessionmaker[Session]) -> InstitutionService:
    persistence = InstitutionPersistenceAdapter(session_factory)
    return InstitutionServiceImpl(persistence)
