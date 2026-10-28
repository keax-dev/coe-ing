# Tema: pruebas unitarias y de integración con pytest.
# Las pruebas del directorio tests verifican contratos, casos límite y efectos observables.
# Usamos fixtures para datos compartidos, parametrize para entradas y tmp_path para archivos.
# Los mocks aíslan servicios externos; no sustituyen las verificaciones de comportamiento.
# Este archivo ejecuta las pruebas de modelos y servicios; el comando pytest ejecuta todas.
# Ejecuta: .\.venv\Scripts\python.exe lesson_09_automated_testing.py

from pathlib import Path

import pytest


def main() -> int:
    project_root = Path(__file__).resolve().parent
    return int(
        pytest.main(
            [
                str(project_root / "tests" / "test_models.py"),
                str(project_root / "tests" / "test_services.py"),
                "-q",
            ]
        )
    )


if __name__ == "__main__":
    raise SystemExit(main())
