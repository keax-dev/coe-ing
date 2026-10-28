# Tema: restricciones reales del modelo de persistencia y de su clave foránea.

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, sessionmaker

from src.education.clean.domain.model.education import Education
from src.education.clean.infrastructure.mapper.education_persistence_mapper import (
    EducationPersistenceMapper,
)
from src.education.clean.infrastructure.model.education_model import EducationModel


def test_model_identifies_table_and_foreign_key() -> None:
    assert EducationModel.__tablename__ == "education"
    references = {
        key.target_fullname for key in EducationModel.__table__.c.institution_id.foreign_keys
    }
    assert references == {"institution.institution_id"}


def test_database_rejects_orphan_education(session_factory: sessionmaker[Session]) -> None:
    entity = Education(
        education_title="Degree",
        education_place="Quito",
        education_end="Present",
        education_position=0,
        institution_id=999999,
    )
    with pytest.raises(IntegrityError):
        with session_factory.begin() as session:
            session.add(EducationPersistenceMapper.to_record(entity))
