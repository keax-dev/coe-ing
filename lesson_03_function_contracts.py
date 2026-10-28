# Tema: firmas, alcance, parámetros por nombre, *args, **kwargs y efectos secundarios.

from collections.abc import Iterable
from decimal import Decimal

from expense_tracker.models import Category, Expense
from expense_tracker.sample_data import sample_expenses
from expense_tracker.services import filter_expenses


def combine_expenses(*groups: Iterable[Expense]) -> list[Expense]:
    # *groups acepta varias colecciones y los dos recorridos las aplanan en una sola lista.
    return [expense for group in groups for expense in group]


def build_metadata(**fields: str) -> dict[str, str]:
    # **fields reúne los argumentos nombrados en un diccionario.
    return {key: value.strip() for key, value in fields.items()}


def with_expense(expense: Expense, expenses: list[Expense] | None = None) -> list[Expense]:
    # None evita compartir una lista predeterminada entre llamadas; no modificamos la recibida.
    # Los modelos Expense son inmutables; una nueva lista basta para este caso.
    return [*(expenses if expenses is not None else []), expense]


def main() -> None:
    expenses = sample_expenses()
    # category y minimum son parámetros que filter_expenses exige pasar por nombre.
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
