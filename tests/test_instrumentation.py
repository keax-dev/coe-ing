# Tema: pruebas del contrato del decorador.

import logging

import pytest

from expense_tracker.instrumentation import timed


def test_decorator_keeps_metadata_and_result() -> None:
    @timed
    def add(left: int, right: int) -> int:
        return left + right

    assert add(2, right=3) == 5
    assert add.__name__ == "add"


def test_decorator_logs_and_propagates_errors(caplog: pytest.LogCaptureFixture) -> None:
    @timed
    def fail() -> None:
        raise ValueError("Expected failure")

    # caplog captura el registro mientras verificamos que el decorador no oculte la excepción.
    with caplog.at_level(logging.INFO), pytest.raises(ValueError, match="Expected failure"):
        fail()
    assert "fail completed" in caplog.text
