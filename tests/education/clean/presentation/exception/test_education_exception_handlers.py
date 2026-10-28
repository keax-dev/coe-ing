# Tema: errores REST de educación sin exposición de SQL ni credenciales.

from unittest.mock import Mock

from fastapi.testclient import TestClient
from sqlalchemy.exc import OperationalError

from src.education.clean.domain.exception.education_errors import EducationPersistenceConflict
from src.main import create_app


def test_database_error_returns_503_without_details() -> None:
    factory = Mock()
    factory.return_value.begin.side_effect = OperationalError("hidden SQL", {}, Exception("secret"))
    with TestClient(create_app(factory)) as client:
        response = client.get("/api/v1/educations")
    assert response.status_code == 503
    assert "secret" not in response.text and "hidden SQL" not in response.text


def test_conflict_returns_409() -> None:
    app = create_app(Mock())
    app.state.education_service = Mock()
    app.state.education_service.get.side_effect = EducationPersistenceConflict(
        "Education violates a database constraint."
    )
    with TestClient(app) as client:
        response = client.get("/api/v1/educations/1")
    assert response.status_code == 409
    assert response.json()["code"] == "EDUCATION_PERSISTENCE_CONFLICT"
