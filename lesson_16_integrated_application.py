# Tema: integración de modelos, servicios, repositorio y comandos de terminal.
# Esta demostración usa la misma interfaz que expense-tracker y python -m expense_tracker.
# Creamos gastos, consultamos resúmenes y exportamos registros en una base temporal.
# Los errores de validación se traducen en códigos de salida sin guardar datos inválidos.
# Ejecuta: .\.venv\Scripts\python.exe lesson_16_integrated_application.py

from pathlib import Path
from tempfile import TemporaryDirectory

from expense_tracker.cli import main as run_command


def main() -> None:
    with TemporaryDirectory() as directory:
        database = Path(directory) / "expenses.db"
        export_path = Path(directory) / "expenses.json"
        prefix = ["--database", str(database)]
        commands = [
            ["add", "Team lunch", "12.50", "--category", "food", "--date", "2026-10-01"],
            ["add", "Bus", "3.00", "--category", "transport"],
            ["list"],
            ["summary", "--budget", "50.00"],
            ["export-json", str(export_path)],
            ["add", "Invalid expense", "-1.00"],
        ]
        for command in commands:
            print("\nCommand:", " ".join(command))
            print("Exit code:", run_command([*prefix, *command]))
        print("Export exists:", export_path.exists())


if __name__ == "__main__":
    main()
