# El protocolo define el contrato; SQLite lo implementa sin acoplar los servicios a SQL.
# La conexión se cierra con closing; el bloque with de sqlite confirma o revierte cambios.

import sqlite3
from collections.abc import Iterable
from contextlib import closing
from pathlib import Path
from typing import Protocol

from expense_tracker.errors import StorageError
from expense_tracker.models import Expense
from expense_tracker.serialization import expense_from_record, expense_to_record


class ExpenseRepository(Protocol):
    def add(self, expense: Expense) -> None: ...

    def list_all(self) -> list[Expense]: ...


class SQLiteExpenseRepository:
    def __init__(self, path: Path) -> None:
        self.path = path
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            with closing(sqlite3.connect(path)) as connection, connection:
                connection.execute(
                    "CREATE TABLE IF NOT EXISTS expenses ("
                    "expense_id TEXT PRIMARY KEY, description TEXT NOT NULL, "
                    "amount TEXT NOT NULL, category TEXT NOT NULL, spent_on TEXT NOT NULL)"
                )
        except (OSError, sqlite3.Error) as error:
            raise StorageError(f"Cannot initialize expense database: {error}") from error

    def add(self, expense: Expense) -> None:
        self.add_many([expense])

    def add_many(self, expenses: Iterable[Expense]) -> None:
        records = [expense_to_record(expense) for expense in expenses]
        try:
            with closing(sqlite3.connect(self.path)) as connection, connection:
                connection.executemany(
                    "INSERT INTO expenses VALUES "
                    "(:expense_id, :description, :amount, :category, :spent_on)",
                    records,
                )
        except sqlite3.Error as error:
            raise StorageError(f"Cannot save expenses: {error}") from error

    def list_all(self) -> list[Expense]:
        try:
            with closing(sqlite3.connect(self.path)) as connection:
                connection.row_factory = sqlite3.Row
                rows = connection.execute(
                    "SELECT * FROM expenses ORDER BY spent_on, expense_id"
                ).fetchall()
                return [expense_from_record(dict(row)) for row in rows]
        except sqlite3.Error as error:
            raise StorageError(f"Cannot read expenses: {error}") from error

    def delete(self, expense_id: str) -> bool:
        try:
            with closing(sqlite3.connect(self.path)) as connection, connection:
                cursor = connection.execute(
                    "DELETE FROM expenses WHERE expense_id = ?", (expense_id,)
                )
                return cursor.rowcount > 0
        except sqlite3.Error as error:
            raise StorageError(f"Cannot delete expense: {error}") from error

    def update_description(self, expense_id: str, description: str) -> bool:
        if not description.strip():
            raise ValueError("Description cannot be empty.")
        try:
            with closing(sqlite3.connect(self.path)) as connection, connection:
                cursor = connection.execute(
                    "UPDATE expenses SET description = ? WHERE expense_id = ?",
                    (description.strip(), expense_id),
                )
                return cursor.rowcount > 0
        except sqlite3.Error as error:
            raise StorageError(f"Cannot update expense: {error}") from error
