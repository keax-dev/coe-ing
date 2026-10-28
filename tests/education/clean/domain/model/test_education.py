# Tema: validación de la entidad de educación sin frameworks.

from dataclasses import FrozenInstanceError

import pytest

from src.education.clean.domain.exception.education_errors import InvalidEducation
from src.education.clean.domain.model.education import Education

VALID = dict(
    education_title="Degree",
    education_place="Quito",
    education_end="Present",
    education_position=0,
    institution_id=1,
)


@pytest.mark.parametrize(
    "changes",
    [
        {"education_title": " "},
        {"education_place": ""},
        {"education_end": " "},
        {"education_title_es": "x" * 256},
        {"education_start": "x" * 256},
        {"education_position": True},
        {"education_position": 2**31},
        {"institution_id": 0},
        {"institution_id": True},
        {"education_visible": "true"},
        {"version": -1},
    ],
)
def test_invalid_state_is_rejected(changes: dict) -> None:
    with pytest.raises(InvalidEducation):
        Education(**(VALID | changes))


def test_defaults_text_dates_and_immutability() -> None:
    education = Education(**VALID, education_start="September 2020")
    assert education.education_visible is True
    assert education.education_deleted is False
    assert education.education_start == "September 2020"
    assert education.education_end == "Present"
    with pytest.raises(FrozenInstanceError):
        setattr(education, "institution_id", 2)
