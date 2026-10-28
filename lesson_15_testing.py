# Tema: pruebas con pytest, parametrización, fixtures y simulación de dependencias.

import json
from collections.abc import Callable
from pathlib import Path

import pytest


def average_score(scores: list[int]) -> float:
    if not scores:
        raise ValueError("At least one score is required.")
    return sum(scores) / len(scores)


def build_greeting(name: str, read_language: Callable[[], str]) -> str:
    # La dependencia se recibe como función para poder sustituirla sin consultar servicios reales.
    language = read_language()
    return f"Hello, {name}!" if language == "en" else f"Welcome, {name}!"


def read_language() -> str:
    return "en"


@pytest.fixture
def scores() -> list[int]:
    # pytest entrega una lista nueva a cada prueba que declara este parámetro.
    return [80, 90, 100]


def test_known_average(scores: list[int]) -> None:
    assert average_score(scores) == 90.0


@pytest.mark.parametrize(
    "values, expected", [([50], 50.0), ([0, 100], 50.0), ([75, 85], 80.0)]
)
def test_average_cases(values: list[int], expected: float) -> None:
    # La misma prueba se ejecuta una vez por cada combinación de entradas y salida esperada.
    assert average_score(values) == expected


def test_empty_input() -> None:
    with pytest.raises(ValueError, match="At least one"):
        average_score([])


def test_temporary_file(tmp_path: Path, scores: list[int]) -> None:
    # tmp_path aísla la escritura y pytest administra la carpeta de la prueba.
    path = tmp_path / "scores.json"
    path.write_text(json.dumps(scores), encoding="utf-8")
    assert json.loads(path.read_text(encoding="utf-8")) == scores


def test_dependency_substitution(monkeypatch: pytest.MonkeyPatch) -> None:
    # Sustituimos una función del propio archivo; no importamos otros ejemplos.
    monkeypatch.setitem(globals(), "read_language", lambda: "other")
    assert build_greeting("Alex", read_language) == "Welcome, Alex!"


if __name__ == "__main__":
    # pytest importa este mismo archivo para descubrir las pruebas sin volver a ejecutar este bloque.
    raise SystemExit(pytest.main([str(Path(__file__).resolve()), "-q"]))
