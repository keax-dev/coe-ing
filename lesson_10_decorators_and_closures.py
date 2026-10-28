# Tema: cierres, fábricas de funciones, decoradores y preservación de metadatos.

import logging
from collections.abc import Callable, Iterable
from decimal import Decimal

from expense_tracker.instrumentation import timed
from expense_tracker.models import Expense
from expense_tracker.sample_data import sample_expenses
from expense_tracker.services import total_amount


def minimum_amount(threshold: Decimal) -> Callable[[Expense], bool]:
    # matches conserva threshold aunque minimum_amount ya haya terminado.
    def matches(expense: Expense) -> bool:
        return expense.amount >= threshold

    return matches


@timed
def calculate_report(expenses: Iterable[Expense]) -> Decimal:
    # @timed añade medición y registros sin mezclar esa tarea con el cálculo del reporte.
    return total_amount(expenses)


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    expenses = sample_expenses()
    is_large = minimum_amount(Decimal("10.00"))
    # Cada cierre conserva su propio umbral.
    is_small_or_large = minimum_amount(Decimal("2.00"))
    print("Large expenses:", [expense.description for expense in filter(is_large, expenses)])
    print("Independent closure count:", len(list(filter(is_small_or_large, expenses))))
    print("Report total:", calculate_report(expenses))
    print("Preserved function name:", calculate_report.__name__)


if __name__ == "__main__":
    main()
