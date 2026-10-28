# Tema: cierres, decoradores y preservación de firmas y metadatos.

from collections.abc import Callable
from functools import wraps
from time import perf_counter
from typing import ParamSpec, TypeVar

Parameters = ParamSpec("Parameters")
Result = TypeVar("Result")


def minimum_score(threshold: int) -> Callable[[int], bool]:
    # El cierre conserva threshold después de que la función exterior termina.
    def matches(score: int) -> bool:
        return score >= threshold

    return matches


def timed(function: Callable[Parameters, Result]) -> Callable[Parameters, Result]:
    # ParamSpec conserva los argumentos y TypeVar conserva el tipo del resultado.
    @wraps(function)
    def wrapper(*args: Parameters.args, **kwargs: Parameters.kwargs) -> Result:
        started_at = perf_counter()
        try:
            return function(*args, **kwargs)
        finally:
            # La medición ocurre incluso si la función envuelta produce un error.
            print(
                f"{function.__name__} completed in {perf_counter() - started_at:.6f} seconds"
            )

    return wrapper


@timed
def calculate_average(scores: list[int]) -> float:
    if not scores:
        raise ValueError("At least one score is required.")
    return sum(scores) / len(scores)


def main() -> None:
    scores = [60, 85, 92]
    is_passing = minimum_score(80)
    is_excellent = minimum_score(90)
    print("Passing scores:", list(filter(is_passing, scores)))
    print("Excellent scores:", list(filter(is_excellent, scores)))
    print("Average:", calculate_average(scores))
    # wraps impide que el nombre público termine siendo wrapper.
    print("Preserved name:", calculate_average.__name__)
    try:
        calculate_average([])
    except ValueError as error:
        print("Original error preserved:", error)


if __name__ == "__main__":
    main()
