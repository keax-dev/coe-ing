# Tema: contratos JSON y rechazo de campos administrados por el servidor.

import pytest
from pydantic import ValidationError

from src.education.clean.presentation.schema.education_schema import (
    EducationCreateRequest,
    EducationUpdateRequest,
)

VALID = dict(
    educationTitle="Degree",
    educationPlace="Quito",
    educationEnd="Present",
    educationPosition=0,
    institutionId=1,
)


def test_schema_aliases_defaults_and_text_dates() -> None:
    request = EducationCreateRequest.model_validate(VALID | {"educationStart": "September 2020"})
    assert request.education_visible is True
    assert request.education_start == "September 2020"
    assert request.model_dump(by_alias=True)["institutionId"] == 1


@pytest.mark.parametrize("extra", [{"educationId": 1}, {"educationDeleted": True}, {"version": 0}])
def test_create_rejects_server_fields(extra: dict) -> None:
    with pytest.raises(ValidationError):
        EducationCreateRequest.model_validate(VALID | extra)


def test_update_requires_integer_version() -> None:
    with pytest.raises(ValidationError):
        EducationUpdateRequest.model_validate(VALID)
    with pytest.raises(ValidationError):
        EducationUpdateRequest.model_validate(VALID | {"version": True})
