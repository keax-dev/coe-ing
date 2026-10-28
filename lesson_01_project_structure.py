# Tema: estructura de un proyecto intermedio, paquetes y dependencias.
# Asumimos que ya conoces variables, condiciones, bucles y funciones básicas.
# src contiene el paquete instalable; tests comprueba contratos y casos límite.
# pyproject.toml declara dependencias, comandos de terminal y herramientas de calidad.
# Instalación: py -m venv .venv
# Después: .\.venv\Scripts\python.exe -m pip install -e ".[dev]"
# Ejecuta: .\.venv\Scripts\python.exe lesson_01_project_structure.py

from importlib.metadata import version
from pathlib import Path

from expense_tracker import __version__
from expense_tracker.sample_data import sample_expenses
from expense_tracker.services import total_amount


def main() -> None:
    project_root = Path(__file__).resolve().parent
    print("Course version:", __version__)
    print("Installed distribution:", version("coe-ing-expense-tracker"))
    print("Package directory:", project_root / "src" / "expense_tracker")
    print("Test directory:", project_root / "tests")
    print("Sample total:", total_amount(sample_expenses()))


if __name__ == "__main__":
    main()
