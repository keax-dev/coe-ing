# Tema: validación e inmutabilidad del modelo de dominio.

from dataclasses import FrozenInstanceError

import pytest

from src.institution.domain.exception.institution_errors import InvalidInstitution
from src.institution.domain.model.institution import Institution


@pytest.mark.parametrize(
    "fields",
    [
        {"institution_name": " "},
        {"institution_name": "x" * 256},
        {"institution_name": "Valid", "institution_name_es": "x" * 256},
        {"institution_name": "Valid", "institution_url": "x" * 2049},
        {"institution_name": "Valid", "institution_id": 0},
        {"institution_name": "Valid", "version": -1},
    ],
)
def test_invalid_domain_state_is_rejected(fields: dict) -> None:
    # Las reglas deben cumplirse incluso si el modelo se construye sin pasar por HTTP.
    with pytest.raises(InvalidInstitution):
        Institution(**fields)


def test_domain_model_is_immutable() -> None:
    institution = Institution(institution_name="University")
    with pytest.raises(FrozenInstanceError):
        setattr(institution, "institution_name", "Changed")
