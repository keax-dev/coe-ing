# Tema: estructura de un proyecto intermedio, paquetes y dependencias.

from importlib.metadata import version
from pathlib import Path

from expense_tracker import __version__
from expense_tracker.sample_data import sample_expenses
from expense_tracker.services import total_amount


def main() -> None:
    # __file__ ubica este archivo; parent obtiene la raíz sin depender de la terminal actual.
    project_root = Path(__file__).resolve().parent
    print("Course version:", __version__)
    # Consulta los metadatos que pip registró al instalar el proyecto en modo editable.
    print("Installed distribution:", version("coe-ing-expense-tracker"))
    print("Package directory:", project_root / "src" / "expense_tracker")
    print("Test directory:", project_root / "tests")
    # La lección reutiliza datos y cálculos del paquete en lugar de duplicar sus implementaciones.
    print("Sample total:", total_amount(sample_expenses()))


if __name__ == "__main__":
    main()
