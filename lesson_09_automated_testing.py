# Tema: pruebas unitarias y de integración con pytest.

from pathlib import Path

import pytest


def main() -> int:
    project_root = Path(__file__).resolve().parent
    # Ejecutamos solo modelos y servicios para no volver a invocar la prueba de esta lección.
    # El código de salida de pytest permite detectar fallos desde la terminal.
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
