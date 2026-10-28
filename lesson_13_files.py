# Tema: archivos de texto, JSON, rutas y administradores de contexto.
# Guardaremos el registro como JSON y un resumen como texto.
# with cierra los archivos incluso si ocurre un error.
# JSON conserva listas y diccionarios para recuperarlos en otra ejecución.
# La demostración usa una carpeta temporal que se elimina automáticamente.
# Ejecuta: python lesson_13_files.py

import json
from pathlib import Path
from tempfile import TemporaryDirectory

from lesson_10_functions import calculate_total, create_expense, format_money


def save_expenses(expenses, file_path):
    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open("w", encoding="utf-8") as file:
        json.dump(expenses, file, indent=2, ensure_ascii=False)


def load_expenses(file_path):
    with Path(file_path).open("r", encoding="utf-8") as file:
        expenses = json.load(file)

    # Un JSON válido puede tener una estructura incorrecta para nuestra aplicación.
    if not isinstance(expenses, list):
        raise ValueError("Saved data must be a list of expenses.")
    for expense in expenses:
        if not isinstance(expense, dict):
            raise ValueError("Each expense must be an object.")
        if not isinstance(expense.get("description"), str) or not expense["description"].strip():
            raise ValueError("Each expense must have a description.")
        if not isinstance(expense.get("category"), str) or not expense["category"].strip():
            raise ValueError("Each expense must have a category.")
        # bool es una subclase de int; usamos type para rechazar true y false del JSON.
        if type(expense.get("amount_cents")) is not int or expense["amount_cents"] <= 0:
            raise ValueError("Each expense must have a positive integer amount.")
    return expenses


if __name__ == "__main__":
    expenses = [create_expense("Lunch", 1250, "food"), create_expense("Bus", 300, "transport")]
    with TemporaryDirectory() as temporary_directory:
        data_path = Path(temporary_directory) / "expenses.json"
        report_path = Path(temporary_directory) / "summary.txt"
        save_expenses(expenses, data_path)
        restored_expenses = load_expenses(data_path)

        with report_path.open("w", encoding="utf-8") as file:
            file.write(f"Total: {format_money(calculate_total(restored_expenses))}\n")
        with report_path.open("r", encoding="utf-8") as file:
            print(file.read(), end="")

        print("Restored expenses:", restored_expenses)
        print("JSON content:", data_path.read_text(encoding="utf-8"))

# Práctica:
# 1. Agrega el número de gastos al informe de texto.
# 2. Cambia la ruta temporal por una ruta propia para conservar el archivo.
# 3. Modifica el JSON antes de cargarlo y observa la validación de su estructura.
