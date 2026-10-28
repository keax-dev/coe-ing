# Tema: excepciones del dominio, encadenamiento, contexto y registros de ejecución.
# Una excepción específica permite reaccionar sin capturar indiscriminadamente cualquier fallo.
# contextmanager garantiza una acción de cierre mediante finally.
# logging registra eventos sin mezclar esa responsabilidad con el cálculo del resultado.
# Ejecuta: .\.venv\Scripts\python.exe lesson_08_errors_and_contexts.py

import logging
from collections.abc import Iterator
from contextlib import contextmanager

from expense_tracker.errors import ExpenseValidationError
from expense_tracker.models import parse_money

logger = logging.getLogger(__name__)


@contextmanager
def operation_scope(name: str) -> Iterator[None]:
    logger.info("Starting operation: %s", name)
    try:
        yield
    except ExpenseValidationError:
        logger.warning("Validation failed: %s", name)
        raise
    finally:
        logger.info("Closing operation: %s", name)


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    for raw_amount in ["12.50", "invalid", "-3.00"]:
        try:
            with operation_scope("parse amount"):
                print("Accepted amount:", parse_money(raw_amount))
        except ExpenseValidationError as error:
            print("Handled domain error:", error)
            if error.__cause__ is not None:
                print("Original error type:", type(error.__cause__).__name__)


if __name__ == "__main__":
    main()
