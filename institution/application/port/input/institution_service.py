# Tema: puerto de entrada con los casos de uso del CRUD.

from typing import Protocol

from institution.domain.model.institution import Institution


class InstitutionService(Protocol):
    def create(self, institution: Institution) -> Institution: ...

    def get(self, institution_id: int) -> Institution: ...

    def list(self, offset: int, limit: int) -> list[Institution]: ...

    def update(self, institution: Institution) -> Institution: ...

    def delete(self, institution_id: int, version: int) -> None: ...
