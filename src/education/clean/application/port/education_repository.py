# Tema: contrato de acceso a datos definido por los casos de uso.

from typing import Protocol

from src.education.clean.domain.model.education import Education


class EducationRepository(Protocol):
    def create(self, education: Education) -> Education: ...

    def find_by_id(self, education_id: int) -> Education | None: ...

    def find_all(
        self, offset: int, limit: int, institution_id: int | None, visible: bool | None
    ) -> list[Education]: ...

    def update(self, education: Education) -> Education: ...

    def soft_delete(self, education_id: int, version: int) -> None: ...
