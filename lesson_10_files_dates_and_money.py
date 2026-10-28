# Tema: archivos JSON y CSV, fechas y precisión monetaria con Decimal.

import csv
import json
from datetime import date, timedelta
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path
from tempfile import TemporaryDirectory


def main() -> None:
    print("Float arithmetic:", 0.1 + 0.2)
    # Decimal recibe texto para no heredar aproximaciones binarias de un float.
    price = Decimal("12.50")
    rate = Decimal("0.925")
    converted = (price * rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    print("Decimal arithmetic:", Decimal("0.1") + Decimal("0.2"))
    print("Explicit currency rounding:", converted)
    purchase_date = date(2026, 10, 1)
    print("Return deadline:", purchase_date + timedelta(days=30))

    # Guardamos texto decimal e ISO para recuperar dinero y fechas con su significado original.
    records = [
        {"product": "Book", "price": str(price), "date": purchase_date.isoformat()}
    ]
    with TemporaryDirectory() as directory:
        json_path = Path(directory) / "products.json"
        csv_path = Path(directory) / "products.csv"
        json_path.write_text(json.dumps(records, indent=2), encoding="utf-8")
        loaded_records = json.loads(json_path.read_text(encoding="utf-8"))
        restored_price = Decimal(loaded_records[0]["price"])
        restored_date = date.fromisoformat(loaded_records[0]["date"])
        print("Restored values:", restored_price, restored_date)

        # newline evita saltos extra en Windows; with cierra el archivo al terminar.
        with csv_path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["product", "price", "date"])
            writer.writeheader()
            writer.writerows(records)
        with csv_path.open(newline="", encoding="utf-8") as file:
            print("CSV rows:", list(csv.DictReader(file)))
        print("JSON content:", json_path.read_text(encoding="utf-8"))
    print("Temporary files removed:", not json_path.exists())


if __name__ == "__main__":
    main()
