# Tema: adaptador de salida con transacciones y traducción de fallos técnicos.

from collections.abc import Callable
from typing import TypeVar

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker

from institution.application.port.output.institution_persistence_port import (
    InstitutionPersistencePort,
)
from institution.domain.exception.institution_errors import (
    InstitutionNotFound,
    InstitutionPersistenceConflict,
    InstitutionPersistenceFailure,
    InstitutionVersionConflict,
)
from institution.domain.model.institution import Institution
from institution.infrastructure.output.adapter.repository.mapper.institution_persistence_mapper import (
    InstitutionPersistenceMapper,
)
from institution.infrastructure.output.adapter.repository.repository.institution_repository import (
    InstitutionRepository,
)

Result = TypeVar("Result")


class InstitutionPersistenceAdapter(InstitutionPersistencePort):
    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self._session_factory = session_factory
        self._mapper = InstitutionPersistenceMapper()

    def _execute(self, operation: Callable[[InstitutionRepository], Result]) -> Result:
        try:
            # Cada operación abre su transacción y confirma antes de entregar el resultado al servicio.
            with self._session_factory.begin() as session:
                return operation(InstitutionRepository(session))
        except IntegrityError as error:
            raise InstitutionPersistenceConflict(
                "Institution violates a database constraint."
            ) from error
        except SQLAlchemyError as error:
            raise InstitutionPersistenceFailure(
                "Institution persistence is unavailable."
            ) from error

    def create(self, institution: Institution) -> Institution:
        return self._execute(
            lambda repository: self._mapper.to_domain(
                repository.create(self._mapper.to_entity(institution))
            )
        )

    def find_by_id(self, institution_id: int) -> Institution | None:
        def find(repository: InstitutionRepository) -> Institution | None:
            entity = repository.find_by_id(institution_id)
            return self._mapper.to_domain(entity) if entity is not None else None

        return self._execute(find)

    def find_all(self, offset: int, limit: int) -> list[Institution]:
        return self._execute(
            lambda repository: [
                self._mapper.to_domain(entity) for entity in repository.find_all(offset, limit)
            ]
        )

    def _change(self, institution_id: int, version: int, values: dict[str, object]) -> Institution:
        def change(repository: InstitutionRepository) -> Institution:
            entity = repository.update(institution_id, version, values)
            if entity is None:
                if repository.find_by_id(institution_id) is None:
                    raise InstitutionNotFound("Institution was not found.")
                raise InstitutionVersionConflict(
                    "Institution was modified; reload its current version."
                )
            return self._mapper.to_domain(entity)

        return self._execute(change)

    def update(self, institution: Institution) -> Institution:
        assert institution.institution_id is not None and institution.version is not None
        return self._change(
            institution.institution_id,
            institution.version,
            {
                "institution_name": institution.institution_name,
                "institution_name_es": institution.institution_name_es,
                "institution_url": institution.institution_url,
            },
        )

    def soft_delete(self, institution_id: int, version: int) -> None:
        # Equivale al SQLDelete de Hibernate: mantiene la fila e incrementa version.
        self._change(institution_id, version, {"institution_deleted": True})
