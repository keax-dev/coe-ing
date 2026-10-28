# Tema: rutas, JSON, CSV, fechas y precisión monetaria con Decimal.
# La serialización guarda los montos como texto y las fechas en formato ISO.
# JSON y CSV se convierten de nuevo a modelos validados al importarlos.
# Usamos una carpeta temporal para que la demostración no cambie tus datos.
# Ejecuta: .\.venv\Scripts\python.exe lesson_11_files_dates_and_money.py

from datetime import date, timedelta
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path
from tempfile import TemporaryDirectory

from expense_tracker.sample_data import sample_expenses
from expense_tracker.serialization import export_csv, import_csv, load_json, save_json
from expense_tracker.services import total_amount


def main() -> None:
    expenses = sample_expenses()
    print("Float arithmetic:", 0.1 + 0.2)
    print("Decimal arithmetic:", Decimal("0.1") + Decimal("0.2"))
    converted_amount = (expenses[0].amount * Decimal("0.925")).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )
    print("Converted amount with explicit rounding:", converted_amount)
    cutoff = date(2026, 10, 1) + timedelta(days=2)
    recent = [expense for expense in expenses if expense.spent_on >= cutoff]
    print("Total from cutoff date:", total_amount(recent))

    with TemporaryDirectory() as directory:
        json_path = Path(directory) / "expenses.json"
        csv_path = Path(directory) / "expenses.csv"
        save_json(expenses, json_path)
        export_csv(expenses, csv_path)
        print("JSON round trip:", load_json(json_path) == expenses)
        print("CSV round trip:", import_csv(csv_path) == expenses)
        print("Serialized example:", json_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
