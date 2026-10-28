# Tema: lambda, funciones de orden superior y herramientas funcionales.

from collections.abc import Callable, Iterable
from functools import partial, reduce


def select_scores(
    scores: Iterable[tuple[str, int]], predicate: Callable[[int], bool]
) -> list[tuple[str, int]]:
    # La condición llega como función, por lo que el recorrido admite reglas diferentes.
    return [(name, score) for name, score in scores if predicate(score)]


def meets_threshold(score: int, *, threshold: int) -> bool:
    return score >= threshold


def main() -> None:
    scores = [("Alex", 85), ("Sam", 92), ("Taylor", 78)]
    # Una lambda devuelve una expresión: aquí obtiene la nota usada como clave de ordenamiento.
    ordered_scores = sorted(scores, key=lambda score: score[1])
    print("Scores ordered by grade:", ordered_scores)

    # map transforma y filter selecciona; list consume los iteradores para mostrar sus resultados.
    names = list(map(lambda score: score[0].upper(), scores))
    passed = list(filter(lambda score: score[1] >= 80, scores))
    equivalent = [score for score in scores if score[1] >= 80]
    print("Mapped names:", names)
    print("Equivalent filters:", passed == equivalent)

    # partial fija un argumento; reduce combina elementos a partir del acumulador inicial.
    is_high_score = partial(meets_threshold, threshold=90)
    print("High scores:", select_scores(scores, is_high_score))
    print("Total score:", reduce(lambda total, score: total + score[1], scores, 0))
    # any termina al encontrar un verdadero y all al encontrar un falso.
    print("Any perfect score:", any(score == 100 for _, score in scores))
    print("All scores valid:", all(0 <= score <= 100 for _, score in scores))

    # zip empareja colecciones; strict detecta longitudes distintas y enumerate agrega un índice.
    for number, (name, score) in enumerate(zip(names, scores, strict=True), start=1):
        print(number, name, score[1])


if __name__ == "__main__":
    main()
