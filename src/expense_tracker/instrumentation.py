# El decorador conserva la firma tipada y los metadatos de la función original.
# finally registra el tiempo tanto si la operación termina como si lanza un error.

import logging
from collections.abc import Callable
from functools import wraps
from time import perf_counter
from typing import ParamSpec, TypeVar

Parameters = ParamSpec("Parameters")
Result = TypeVar("Result")
logger = logging.getLogger(__name__)


def timed(function: Callable[Parameters, Result]) -> Callable[Parameters, Result]:
    @wraps(function)
    def wrapper(*args: Parameters.args, **kwargs: Parameters.kwargs) -> Result:
        started_at = perf_counter()
        try:
            return function(*args, **kwargs)
        finally:
            logger.info(
                "%s completed in %.6f seconds", function.__name__, perf_counter() - started_at
            )

    return wrapper
