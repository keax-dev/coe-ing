# Cada lección debe poder ejecutarse desde terminal con el entorno instalado.
# La lección 09 solo ejecuta modelos y servicios; no vuelve a invocar esta prueba.

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
LESSONS = sorted(ROOT.glob("lesson_*.py"))


@pytest.mark.parametrize("lesson", LESSONS, ids=lambda path: path.name)
def test_lesson_runs_without_network(lesson: Path) -> None:
    result = subprocess.run(
        [sys.executable, "-B", str(lesson)], cwd=ROOT, capture_output=True, text=True, timeout=60
    )
    assert result.returncode == 0, result.stdout + result.stderr
