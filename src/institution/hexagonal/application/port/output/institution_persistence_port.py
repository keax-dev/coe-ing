# Tema: puerto de salida para persistir modelos de dominio.

from typing import Protocol

from src.institution.hexagonal.domain.model.institution import Institution


class InstitutionPersistencePort(Protocol):
    def create(self, institution: Institution) -> Institution: ...

    def find_by_id(self, institution_id: int) -> Institution | None: ...

    def find_all(self, offset: int, limit: int) -> list[Institution]: ...

    def update(self, institution: Institution) -> Institution: ...

    def soft_delete(self, institution_id: int, version: int) -> None: ...
