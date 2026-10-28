# Tema: verificación de ejecución de las lecciones.

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
LESSONS = sorted(ROOT.glob("lesson_*.py"))


@pytest.mark.parametrize("lesson", LESSONS, ids=lambda path: path.name)
def test_lesson_runs_without_network(lesson: Path) -> None:
    # Cada archivo se ejecuta como programa independiente con el mismo intérprete de las pruebas.
    # La lección 09 solo prueba modelos y servicios, evitando recursión sobre esta verificación.
    result = subprocess.run(
        [sys.executable, "-B", str(lesson)], cwd=ROOT, capture_output=True, text=True, timeout=60
    )
    assert result.returncode == 0, result.stdout + result.stderr
