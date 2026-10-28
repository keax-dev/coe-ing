# Tema: cierres, fábricas de funciones, decoradores y preservación de metadatos.
# Un cierre conserva valores del alcance donde se creó, como un umbral de filtrado.
# Un decorador envuelve una función para agregar comportamiento reutilizable.
# wraps mantiene el nombre de la función original; ParamSpec conserva su firma estática.
# Ejecuta: .\.venv\Scripts\python.exe lesson_10_decorators_and_closures.py

import logging
from collections.abc import Callable, Iterable
from decimal import Decimal

from expense_tracker.instrumentation import timed
from expense_tracker.models import Expense
from expense_tracker.sample_data import sample_expenses
from expense_tracker.services import total_amount


def minimum_amount(threshold: Decimal) -> Callable[[Expense], bool]:
    def matches(expense: Expense) -> bool:
        return expense.amount >= threshold

    return matches


@timed
def calculate_report(expenses: Iterable[Expense]) -> Decimal:
    return total_amount(expenses)


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    expenses = sample_expenses()
    is_large = minimum_amount(Decimal("10.00"))
    is_small_or_large = minimum_amount(Decimal("2.00"))
    print("Large expenses:", [expense.description for expense in filter(is_large, expenses)])
    print("Independent closure count:", len(list(filter(is_small_or_large, expenses))))
    print("Report total:", calculate_report(expenses))
    print("Preserved function name:", calculate_report.__name__)


if __name__ == "__main__":
    main()
