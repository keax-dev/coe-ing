# Tema: traducción de fallos técnicos a respuestas REST sin filtrar detalles internos.

from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.exc import IntegrityError, OperationalError

from src.main import create_app


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
