# argparse convierte los comandos de terminal en llamadas a servicios reutilizables.
# La interfaz captura errores esperados y devuelve un código de salida significativo.

import argparse
from datetime import date
from pathlib import Path

from expense_tracker.errors import ExpenseTrackerError
from expense_tracker.models import Category, create_expense, format_money, parse_money
from expense_tracker.repositories import SQLiteExpenseRepository
from expense_tracker.serialization import load_json, save_json
from expense_tracker.services import total_amount, totals_by_category


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Track expenses with exact monetary amounts.")
    parser.add_argument("--database", type=Path, default=Path("data/expenses.db"))
    commands = parser.add_subparsers(dest="command", required=True)

    add = commands.add_parser("add", help="Add an expense")
    add.add_argument("description")
    add.add_argument("amount", help="Amount in dollars, for example 12.50")
    add.add_argument(
        "--category", choices=[category.value for category in Category], default="other"
    )
    add.add_argument("--date", dest="spent_on", help="Date in YYYY-MM-DD format")

    commands.add_parser("list", help="List saved expenses")
    summary = commands.add_parser("summary", help="Show totals and remaining budget")
    summary.add_argument("--budget", default="100.00")
    delete = commands.add_parser("delete", help="Delete an expense by its full ID")
    delete.add_argument("expense_id")
    update = commands.add_parser("update", help="Update an expense description")
    update.add_argument("expense_id")
    update.add_argument("description")
    export = commands.add_parser("export-json", help="Export saved expenses")
    export.add_argument("path", type=Path)
    restore = commands.add_parser("import-json", help="Import expenses in one transaction")
    restore.add_argument("path", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        repository = SQLiteExpenseRepository(args.database)
        if args.command == "add":
            spent_on = date.fromisoformat(args.spent_on) if args.spent_on else None
            expense = create_expense(args.description, args.amount, args.category, spent_on)
            repository.add(expense)
            print("Added:", expense.expense_id)
        elif args.command == "list":
            expenses = repository.list_all()
            for expense in expenses:
                print(f"{expense.expense_id} | {expense}")
            if not expenses:
                print("No expenses recorded.")
        elif args.command == "summary":
            budget = parse_money(args.budget)
            expenses = repository.list_all()
            total = total_amount(expenses)
            print("Total:", format_money(total))
            print("Balance:", format_money(budget - total))
            for category, amount in sorted(totals_by_category(expenses).items()):
                print(f"{category.value}: {format_money(amount)}")
        elif args.command == "delete":
            print("Deleted." if repository.delete(args.expense_id) else "Expense not found.")
        elif args.command == "update":
            updated = repository.update_description(args.expense_id, args.description)
            print("Updated." if updated else "Expense not found.")
        elif args.command == "export-json":
            save_json(repository.list_all(), args.path)
            print("Exported to:", args.path)
        elif args.command == "import-json":
            repository.add_many(load_json(args.path))
            print("Import completed.")
    except (ExpenseTrackerError, OSError, ValueError) as error:
        print(f"Error: {error}")
        return 1
    return 0
