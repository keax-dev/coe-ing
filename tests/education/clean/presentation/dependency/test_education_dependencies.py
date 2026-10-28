# Tema: inyección del servicio y creación de sesiones independientes por operación.

from unittest.mock import Mock

from starlette.requests import Request

from src.education.clean.presentation.dependency.education_dependencies import (
    configure_education_service,
    get_education_service,
)
from src.main import create_app


def test_dependency_returns_app_service() -> None:
    app = create_app(Mock())
    request = Request({"type": "http", "app": app})
    assert get_education_service(request) is app.state.education_service


def test_service_operations_use_independent_sessions() -> None:
    first, second = Mock(), Mock()
    first.scalars.return_value = []
    second.scalars.return_value = []
    factory = Mock(side_effect=[first, second])
    service = configure_education_service(factory)
    assert service.list(0, 20) == []
    assert service.list(0, 20) == []
    assert factory.call_count == 2
    first.close.assert_called_once()
    second.close.assert_called_once()
