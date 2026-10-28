# Tema: repositorio SQLAlchemy que consulta y hace flush sin confirmar transacciones.

from dataclasses import asdict

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from src.education.clean.application.port.education_repository import EducationRepository
from src.education.clean.domain.exception.education_errors import (
    EducationNotFound,
    EducationVersionConflict,
)
from src.education.clean.domain.model.education import Education
from src.education.clean.infrastructure.mapper.education_persistence_mapper import (
    EducationPersistenceMapper,
)
from src.education.clean.infrastructure.model.education_model import EducationModel


class SQLAlchemyEducationRepository(EducationRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, education: Education) -> Education:
        record = EducationPersistenceMapper.to_record(education)
        self._session.add(record)
        # flush obtiene el ID y comprueba restricciones, pero no hace commit.
        self._session.flush()
        return EducationPersistenceMapper.to_entity(record)

    @staticmethod
    def _active(education_id: int):
        return select(EducationModel).where(
            EducationModel.education_id == education_id, EducationModel.education_deleted.is_(False)
        )

    def find_by_id(self, education_id: int) -> Education | None:
        record = self._session.scalar(self._active(education_id))
        return EducationPersistenceMapper.to_entity(record) if record is not None else None

    def find_all(
        self, offset: int, limit: int, institution_id: int | None, visible: bool | None
    ) -> list[Education]:
        query = select(EducationModel).where(EducationModel.education_deleted.is_(False))
        if institution_id is not None:
            query = query.where(EducationModel.institution_id == institution_id)
        if visible is not None:
            query = query.where(EducationModel.education_visible.is_(visible))
        query = (
            query.order_by(EducationModel.education_position, EducationModel.education_id)
            .offset(offset)
            .limit(limit)
        )
        return [
            EducationPersistenceMapper.to_entity(record) for record in self._session.scalars(query)
        ]

    def _write(self, education_id: int, version: int, values: dict) -> Education:
        # La comparación de versión y el incremento permanecen atómicos.
        query = (
            update(EducationModel)
            .where(
                EducationModel.education_id == education_id,
                EducationModel.education_deleted.is_(False),
                EducationModel.version == version,
            )
            .values(**values, version=version + 1)
            .returning(EducationModel)
            .execution_options(populate_existing=True)
        )
        record = self._session.scalars(query).one_or_none()
        if record is None:
            if self._session.scalar(self._active(education_id)) is None:
                raise EducationNotFound("Education was not found.")
            raise EducationVersionConflict("Education was modified; reload its current version.")
        return EducationPersistenceMapper.to_entity(record)

    def update(self, education: Education) -> Education:
        assert education.education_id is not None and education.version is not None
        values = asdict(education)
        for name in ["education_id", "education_deleted", "version"]:
            values.pop(name)
        return self._write(education.education_id, education.version, values)

    def soft_delete(self, education_id: int, version: int) -> None:
        self._write(education_id, version, {"education_deleted": True})
