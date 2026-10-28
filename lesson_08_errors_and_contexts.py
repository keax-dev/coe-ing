# Tema: excepciones del dominio, encadenamiento, contexto y registros de ejecución.

import logging
from collections.abc import Iterator
from contextlib import contextmanager

from expense_tracker.errors import ExpenseValidationError
from expense_tracker.models import parse_money

logger = logging.getLogger(__name__)


@contextmanager
def operation_scope(name: str) -> Iterator[None]:
    # logging permite configurar el destino y el nivel de los mensajes fuera de esta función.
    logger.info("Starting operation: %s", name)
    try:
        # El cuerpo del with se ejecuta aquí, mientras el contexto está abierto.
        yield
    except ExpenseValidationError:
        logger.warning("Validation failed: %s", name)
        # Repropagamos el mismo error para que el llamador decida cómo responder.
        raise
    finally:
        # Este cierre ocurre incluso cuando la validación produce una excepción.
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
                # El encadenamiento conserva el error original que provocó el fallo del dominio.
                print("Original error type:", type(error.__cause__).__name__)


if __name__ == "__main__":
    main()
