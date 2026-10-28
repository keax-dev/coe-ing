# Tema: consultas activas y escrituras atómicas con control de versión.

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from src.institution.hexagonal.infrastructure.output.adapter.repository.entity.institution_entity import (
    InstitutionEntity,
)


class InstitutionRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, entity: InstitutionEntity) -> InstitutionEntity:
        self._session.add(entity)
        self._session.flush()
        return entity

    def find_by_id(self, institution_id: int) -> InstitutionEntity | None:
        return self._session.scalar(
            select(InstitutionEntity).where(
                InstitutionEntity.institution_id == institution_id,
                InstitutionEntity.institution_deleted.is_(False),
            )
        )

    def find_all(self, offset: int, limit: int) -> list[InstitutionEntity]:
        statement = (
            select(InstitutionEntity)
            .where(InstitutionEntity.institution_deleted.is_(False))
            .order_by(InstitutionEntity.institution_id)
            .offset(offset)
            .limit(limit)
        )
        return list(self._session.scalars(statement))

    def update(
        self, institution_id: int, version: int, values: dict[str, object]
    ) -> InstitutionEntity | None:
        # La comparación y el incremento suceden en el mismo UPDATE: no hay ventana de lectura/escritura.
        statement = (
            update(InstitutionEntity)
            .where(
                InstitutionEntity.institution_id == institution_id,
                InstitutionEntity.institution_deleted.is_(False),
                InstitutionEntity.version == version,
            )
            .values(**values, version=version + 1)
            .returning(InstitutionEntity)
        )
        return self._session.scalars(statement).one_or_none()
