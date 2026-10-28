# Tema: repositorios, SQL parametrizado, CRUD y transacciones.

from dataclasses import replace
from pathlib import Path
from tempfile import TemporaryDirectory

from expense_tracker.errors import StorageError
from expense_tracker.repositories import ExpenseRepository, SQLiteExpenseRepository
from expense_tracker.sample_data import sample_expenses
from expense_tracker.services import total_amount


def print_report(repository: ExpenseRepository) -> None:
    # Dependemos del contrato del repositorio, no de detalles de SQLite.
    print("Repository total:", total_amount(repository.list_all()))


def main() -> None:
    expenses = sample_expenses()
    # La base temporal permite repetir el ejemplo sin tocar los registros de trabajo.
    with TemporaryDirectory() as directory:
        repository = SQLiteExpenseRepository(Path(directory) / "expenses.db")
        repository.add_many(expenses)
        print_report(repository)
        repository.update_description(expenses[0].expense_id, "Team lunch")
        print("Updated description:", repository.list_all()[0].description)

        new_expense = replace(expenses[0], expense_id="new-expense")
        try:
            # El segundo registro tiene un ID existente; el primero tampoco debe persistir.
            # add_many agrupa ambas inserciones en una sola transacción.
            repository.add_many([new_expense, expenses[1]])
        except StorageError as error:
            print("Transaction rolled back:", error)
        print("Record count after failed transaction:", len(repository.list_all()))
        print("Deleted:", repository.delete(expenses[-1].expense_id))
        print_report(repository)


if __name__ == "__main__":
    main()
