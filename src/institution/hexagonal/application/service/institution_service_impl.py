# Tema: implementación de casos de uso mediante el puerto de persistencia.

from src.institution.hexagonal.application.port.input.institution_service import InstitutionService
from src.institution.hexagonal.application.port.output.institution_persistence_port import (
    InstitutionPersistencePort,
)
from src.institution.hexagonal.domain.exception.institution_errors import (
    InstitutionNotFound,
    InvalidInstitution,
)
from src.institution.hexagonal.domain.model.institution import Institution


class InstitutionServiceImpl(InstitutionService):
    def __init__(self, persistence: InstitutionPersistencePort) -> None:
        self._persistence = persistence

    def create(self, institution: Institution) -> Institution:
        if institution.institution_id is not None or institution.version is not None:
            raise InvalidInstitution("New institutions cannot specify an ID or version.")
        if institution.institution_deleted:
            raise InvalidInstitution("New institutions cannot be deleted.")
        return self._persistence.create(institution)

    def get(self, institution_id: int) -> Institution:
        institution = self._persistence.find_by_id(institution_id)
        if institution is None:
            raise InstitutionNotFound("Institution was not found.")
        return institution

    def list(self, offset: int, limit: int) -> list[Institution]:
        if offset < 0 or not 1 <= limit <= 100:
            raise InvalidInstitution("Pagination requires offset >= 0 and limit between 1 and 100.")
        return self._persistence.find_all(offset, limit)

    def update(self, institution: Institution) -> Institution:
        if institution.institution_id is None or institution.version is None:
            raise InvalidInstitution("Updates require an ID and version.")
        if institution.institution_deleted:
            raise InvalidInstitution("Use the delete operation to delete institutions.")
        return self._persistence.update(institution)

    def delete(self, institution_id: int, version: int) -> None:
        if institution_id <= 0 or version < 0:
            raise InvalidInstitution("Deletion requires a positive ID and nonnegative version.")
        self._persistence.soft_delete(institution_id, version)
