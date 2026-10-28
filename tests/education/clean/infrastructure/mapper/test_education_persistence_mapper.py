# Tema: conversiones de persistencia sin pérdida de campos de negocio.

from dataclasses import replace

from src.education.clean.domain.model.education import Education
from src.education.clean.infrastructure.mapper.education_persistence_mapper import (
    EducationPersistenceMapper,
)


def test_mapper_round_trip_preserves_fields() -> None:
    entity = Education(
        education_title="Degree",
        education_place="Quito",
        education_end="Present",
        education_position=-1,
        institution_id=1,
        education_visible=False,
        education_start="September 2020",
    )
    record = EducationPersistenceMapper.to_record(entity)
    record.education_id = 7
    assert EducationPersistenceMapper.to_entity(record) == replace(
        entity, education_id=7, version=0
    )
