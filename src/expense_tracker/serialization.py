# Serializamos dinero como texto para preservar su valor exacto al leer JSON o CSV.
# Las filas de entrada se validan antes de convertirse en modelos del dominio.

import csv
import json
from collections.abc import Iterable
from datetime import date
from pathlib import Path

from expense_tracker.errors import ExpenseValidationError
from expense_tracker.models import Category, Expense, parse_money

FIELDS = ["expense_id", "description", "amount", "category", "spent_on"]


def expense_to_record(expense: Expense) -> dict[str, str]:
    return {
        "expense_id": expense.expense_id,
        "description": expense.description,
        "amount": str(expense.amount),
        "category": expense.category.value,
        "spent_on": expense.spent_on.isoformat(),
    }


def expense_from_record(record: object) -> Expense:
    if not isinstance(record, dict) or any(not isinstance(record.get(key), str) for key in FIELDS):
        raise ExpenseValidationError("Each expense must contain all required text fields.")
    try:
        return Expense(
            description=record["description"],
            amount=parse_money(record["amount"]),
            category=Category(record["category"]),
            spent_on=date.fromisoformat(record["spent_on"]),
            expense_id=record["expense_id"],
        )
    except ValueError as error:
        raise ExpenseValidationError(f"Invalid expense record: {error}") from error


def save_json(expenses: Iterable[Expense], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps([expense_to_record(expense) for expense in expenses], indent=2),
        encoding="utf-8",
    )


def load_json(path: Path) -> list[Expense]:
    try:
        records = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ExpenseValidationError("Invalid JSON document.") from error
    if not isinstance(records, list):
        raise ExpenseValidationError("Expected a list of expenses.")
    return [expense_from_record(record) for record in records]


def export_csv(expenses: Iterable[Expense], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(expense_to_record(expense) for expense in expenses)


def import_csv(path: Path) -> list[Expense]:
    with path.open(newline="", encoding="utf-8") as file:
        return [expense_from_record(record) for record in csv.DictReader(file)]
