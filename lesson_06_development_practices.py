# Tema: buenas prácticas de desarrollo, funciones puras, validación y pruebas.

import sys
import unittest
from collections.abc import Iterable
from dataclasses import dataclass

PASSING_SCORE = 70
MINIMUM_SCORE = 0
MAXIMUM_SCORE = 100


@dataclass(frozen=True)
class ScoreSummary:
    count: int
    average: float | None
    passed_count: int


def validate_scores(scores: Iterable[int]) -> tuple[int, ...]:
    # Cada función tiene una responsabilidad; esta valida sin modificar la colección original.
    validated = tuple(scores)
    if any(
        type(score) is not int or not MINIMUM_SCORE <= score <= MAXIMUM_SCORE
        for score in validated
    ):
        raise ValueError("Scores must be integers between 0 and 100.")
    return validated


def summarize_scores(scores: Iterable[int]) -> ScoreSummary:
    # Nombres descriptivos, constantes y tipos hacen explícito el contrato de la operación.
    validated = validate_scores(scores)
    return ScoreSummary(
        count=len(validated),
        average=sum(validated) / len(validated) if validated else None,
        passed_count=sum(score >= PASSING_SCORE for score in validated),
    )


class ScoreSummaryTests(unittest.TestCase):
    def test_known_summary_and_unchanged_input(self) -> None:
        scores = [60, 80, 100]
        self.assertEqual(summarize_scores(scores), ScoreSummary(3, 80.0, 2))
        self.assertEqual(scores, [60, 80, 100])

    def test_empty_input_has_no_average(self) -> None:
        self.assertEqual(summarize_scores([]), ScoreSummary(0, None, 0))

    def test_invalid_values_are_rejected(self) -> None:
        # Los casos límite verifican el contrato observable sin reproducir la implementación.
        for scores in [[-1], [101], [True], ["80"]]:
            with self.subTest(scores=scores), self.assertRaises(ValueError):
                summarize_scores(scores)


def main() -> None:
    scores = [60, 80, 100]
    # Separamos el cálculo de la salida: la misma función sirve para terminal u otros consumidores.
    print("Score summary:", summarize_scores(scores))
    print("Original scores preserved:", scores)
    print("Empty summary:", summarize_scores([]))


# Esta protección evita ejecutar la demostración al importar las funciones para verificarlas.
if __name__ == "__main__":
    if "--check" in sys.argv:
        unittest.main(argv=[sys.argv[0]], verbosity=2)
    else:
        main()
