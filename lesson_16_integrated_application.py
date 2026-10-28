# Tema: integración de modelos, servicios, repositorio y comandos de terminal.

from pathlib import Path
from tempfile import TemporaryDirectory

from expense_tracker.cli import main as run_command


def main() -> None:
    # Usamos la misma interfaz que la terminal, con una base y una exportación temporales.
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
            # Un código cero indica éxito; la entrada inválida devuelve uno sin persistir el gasto.
            print("Exit code:", run_command([*prefix, *command]))
        print("Export exists:", export_path.exists())


if __name__ == "__main__":
    main()
