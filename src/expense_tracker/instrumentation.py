# Tema: decoradores tipados y medición de duración.

import logging
from collections.abc import Callable
from functools import wraps
from time import perf_counter
from typing import ParamSpec, TypeVar

Parameters = ParamSpec("Parameters")
Result = TypeVar("Result")
logger = logging.getLogger(__name__)


def timed(function: Callable[Parameters, Result]) -> Callable[Parameters, Result]:
    # ParamSpec y TypeVar conservan los tipos de los argumentos y del resultado.
    @wraps(function)
    def wrapper(*args: Parameters.args, **kwargs: Parameters.kwargs) -> Result:
        # wraps conserva metadatos como __name__ al devolver la función envolvente.
        started_at = perf_counter()
        try:
            return function(*args, **kwargs)
        finally:
            # El tiempo también se registra si la función termina con una excepción.
            logger.info(
                "%s completed in %.6f seconds", function.__name__, perf_counter() - started_at
            )

    return wrapper
