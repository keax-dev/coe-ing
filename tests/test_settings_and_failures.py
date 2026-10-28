# Tema: configuración segura y traducción de errores de infraestructura.

from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.exc import IntegrityError, OperationalError

from institution.application.port.output.institution_persistence_port import (
    InstitutionPersistencePort,
)
from institution.application.service.institution_service_impl import InstitutionServiceImpl
from institution.domain.exception.institution_errors import InvalidInstitution
from institution.domain.model.institution import Institution
from institution.infrastructure.config.settings import Settings
from institution.main import create_app


def test_jdbc_conversion_preserves_special_password_characters() -> None:
    settings = Settings(
        _env_file=None,
        DB_URL="jdbc:postgresql://localhost:5432/portfolio_db",
        DB_USERNAME="postgres",
        DB_PASSWORD="p@ss:/word",
        DB_DRIVER="org.postgresql.Driver",
    )
    assert settings.sqlalchemy_url.drivername == "postgresql+psycopg"
    assert settings.sqlalchemy_url.password == "p@ss:/word"
    assert "p@ss:/word" not in repr(settings)


def test_service_rejects_client_owned_identity() -> None:
    port = Mock(spec=InstitutionPersistencePort)
    service = InstitutionServiceImpl(port)
    with pytest.raises(InvalidInstitution):
        service.create(Institution(institution_name="University", institution_id=1))
    with pytest.raises(InvalidInstitution):
        service.update(Institution(institution_name="University"))
    port.create.assert_not_called()
    port.update.assert_not_called()


@pytest.mark.parametrize(
    "error, expected",
    [
        (OperationalError("hidden SQL", {}, Exception("secret")), 503),
        (IntegrityError("hidden SQL", {}, Exception("secret")), 409),
    ],
)
def test_database_errors_do_not_leak_sql_or_credentials(error: Exception, expected: int) -> None:
    factory = Mock()
    factory.begin.side_effect = error
    app = create_app(factory)
    with TestClient(app) as client:
        response = client.get("/api/v1/institutions")
        assert response.status_code == expected
        assert "secret" not in response.text
        assert "hidden SQL" not in response.text
