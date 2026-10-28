# Tema: contratos y validaciones del servicio de aplicación.

from unittest.mock import Mock

import pytest

from src.institution.application.port.output.institution_persistence_port import (
    InstitutionPersistencePort,
)
from src.institution.application.service.institution_service_impl import InstitutionServiceImpl
from src.institution.domain.exception.institution_errors import InvalidInstitution
from src.institution.domain.model.institution import Institution


def test_service_rejects_client_owned_identity() -> None:
    port = Mock(spec=InstitutionPersistencePort)
    service = InstitutionServiceImpl(port)
    with pytest.raises(InvalidInstitution):
        service.create(Institution(institution_name="University", institution_id=1))
    with pytest.raises(InvalidInstitution):
        service.update(Institution(institution_name="University"))
    port.create.assert_not_called()
    port.update.assert_not_called()
