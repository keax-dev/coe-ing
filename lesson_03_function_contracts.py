# Tema: firmas, alcance, parámetros por nombre, *args, **kwargs y efectos secundarios.
# Los argumentos después de * deben pasarse por nombre para hacer explícita la intención.
# Una función pura devuelve resultados sin cambiar la lista original.
# Un valor predeterminado None evita compartir una lista mutable entre llamadas.
# Ejecuta: .\.venv\Scripts\python.exe lesson_03_function_contracts.py

from collections.abc import Iterable
from decimal import Decimal

from expense_tracker.models import Category, Expense
from expense_tracker.sample_data import sample_expenses
from expense_tracker.services import filter_expenses


def combine_expenses(*groups: Iterable[Expense]) -> list[Expense]:
    return [expense for group in groups for expense in group]


def build_metadata(**fields: str) -> dict[str, str]:
    return {key: value.strip() for key, value in fields.items()}


def with_expense(expense: Expense, expenses: list[Expense] | None = None) -> list[Expense]:
    # Los modelos Expense son inmutables; una nueva lista basta para este caso.
    return [*(expenses if expenses is not None else []), expense]


def main() -> None:
    expenses = sample_expenses()
    selected = filter_expenses(expenses, category=Category.FOOD, minimum=Decimal("3.00"))
    updated = with_expense(expenses[0], expenses)
    print("Filtered descriptions:", [expense.description for expense in selected])
    print("Original and new counts:", len(expenses), len(updated))
    print("Combined count:", len(combine_expenses(expenses[:2], expenses[2:])))
    print("Metadata:", build_metadata(owner=" Alex ", source=" manual "))
    first_call = with_expense(expenses[0])
    second_call = with_expense(expenses[1])
    print("Independent default calls:", first_call is not second_call)


if __name__ == "__main__":
    main()
