# Probamos los comandos como los usa la terminal y verificamos sus efectos persistentes.

from pathlib import Path

import pytest

from expense_tracker.cli import main
from expense_tracker.errors import StorageError
from expense_tracker.repositories import SQLiteExpenseRepository


def test_add_summary_export_and_import(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    database = tmp_path / "first.db"
    prefix = ["--database", str(database)]
    assert main([*prefix, "add", "Lunch", "12.50", "--category", "food"]) == 0
    assert main([*prefix, "summary", "--budget", "10.00"]) == 0
    assert "Balance: -$2.50" in capsys.readouterr().out
    export_path = tmp_path / "backup.json"
    assert main([*prefix, "export-json", str(export_path)]) == 0
    restored_database = tmp_path / "restored.db"
    assert main(["--database", str(restored_database), "import-json", str(export_path)]) == 0
    assert len(SQLiteExpenseRepository(restored_database).list_all()) == 1


@pytest.mark.parametrize("amount", ["-1", "NaN", "1.001"])
def test_invalid_add_does_not_persist(tmp_path: Path, amount: str) -> None:
    database = tmp_path / "expenses.db"
    assert main(["--database", str(database), "add", "Lunch", amount]) == 1
    assert SQLiteExpenseRepository(database).list_all() == []


def test_storage_failure_returns_error(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    def unavailable(path: Path) -> SQLiteExpenseRepository:
        raise StorageError("Database unavailable")

    monkeypatch.setattr("expense_tracker.cli.SQLiteExpenseRepository", unavailable)
    assert main(["--database", str(tmp_path / "expenses.db"), "list"]) == 1
    assert "Database unavailable" in capsys.readouterr().out


def test_update_and_delete(tmp_path: Path) -> None:
    database = tmp_path / "expenses.db"
    prefix = ["--database", str(database)]
    main([*prefix, "add", "Lunch", "12.50"])
    repository = SQLiteExpenseRepository(database)
    expense_id = repository.list_all()[0].expense_id
    assert main([*prefix, "update", expense_id, "Team lunch"]) == 0
    assert repository.list_all()[0].description == "Team lunch"
    assert main([*prefix, "delete", expense_id]) == 0
    assert repository.list_all() == []
