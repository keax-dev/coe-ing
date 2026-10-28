# Tema: pruebas de archivos, SQLite y transacciones.

from dataclasses import replace
from pathlib import Path

import pytest

from expense_tracker.errors import ExpenseValidationError, StorageError
from expense_tracker.models import Expense
from expense_tracker.repositories import SQLiteExpenseRepository
from expense_tracker.serialization import export_csv, import_csv, load_json, save_json


def test_json_and_csv_round_trip(tmp_path: Path, expenses: list[Expense]) -> None:
    # tmp_path proporciona una carpeta aislada; comprobamos la recuperación completa de los modelos.
    json_path = tmp_path / "nested" / "expenses.json"
    csv_path = tmp_path / "expenses.csv"
    save_json(expenses, json_path)
    export_csv(expenses, csv_path)
    assert load_json(json_path) == expenses
    assert import_csv(csv_path) == expenses


@pytest.mark.parametrize("content", ["not JSON", "{}", "[{}]", '[{"amount": true}]'])
def test_bad_json_is_rejected(tmp_path: Path, content: str) -> None:
    path = tmp_path / "invalid.json"
    path.write_text(content, encoding="utf-8")
    with pytest.raises(ExpenseValidationError):
        load_json(path)


def test_database_crud_and_reopening(tmp_path: Path, expenses: list[Expense]) -> None:
    path = tmp_path / "expenses.db"
    repository = SQLiteExpenseRepository(path)
    repository.add_many(expenses)
    reopened = SQLiteExpenseRepository(path)
    assert reopened.list_all() == expenses
    assert reopened.update_description(expenses[0].expense_id, "Team lunch")
    assert reopened.list_all()[0].description == "Team lunch"
    assert reopened.delete(expenses[0].expense_id)
    assert not reopened.delete("missing")
    assert len(reopened.list_all()) == 3


def test_failed_batch_rolls_back_all_rows(tmp_path: Path, expenses: list[Expense]) -> None:
    repository = SQLiteExpenseRepository(tmp_path / "expenses.db")
    repository.add(expenses[0])
    new_expense = replace(expenses[1], expense_id="new-expense")
    # El ID duplicado del segundo elemento debe impedir que persista también el primero.
    with pytest.raises(StorageError):
        repository.add_many([new_expense, expenses[0]])
    assert repository.list_all() == [expenses[0]]


def test_sql_parameters_handle_literal_text(tmp_path: Path, expenses: list[Expense]) -> None:
    # Texto con apariencia de SQL debe guardarse como dato, sin ejecutarse como instrucciones.
    repository = SQLiteExpenseRepository(tmp_path / "expenses.db")
    description = "Lunch'); DROP TABLE expenses; --"
    repository.add(replace(expenses[0], description=description))
    assert repository.list_all()[0].description == description
    assert not repository.delete("' OR 1=1 --")
    assert len(repository.list_all()) == 1
