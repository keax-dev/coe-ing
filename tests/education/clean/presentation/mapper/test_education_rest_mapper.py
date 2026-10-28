# Tema: conversión de contratos REST a dominio y de dominio a respuesta.

from dataclasses import replace

from src.education.clean.presentation.mapper.education_rest_mapper import EducationRestMapper
from src.education.clean.presentation.schema.education_schema import (
    EducationCreateRequest,
    EducationUpdateRequest,
)


def test_mapper_preserves_identity_version_and_optional_fields() -> None:
    values = dict(
        education_title="Degree",
        education_place="Quito",
        education_end="Present",
        education_position=0,
        institution_id=1,
        education_visible=False,
    )
    entity = EducationRestMapper.from_create(EducationCreateRequest(**values))
    assert entity.education_id is None and entity.version is None
    changed = EducationRestMapper.from_update(7, EducationUpdateRequest(**values, version=3))
    assert changed.education_id == 7 and changed.version == 3
    response = EducationRestMapper.to_response(replace(changed, version=4))
    assert response.model_dump(by_alias=True)["educationId"] == 7
    assert response.version == 4 and response.education_visible is False
