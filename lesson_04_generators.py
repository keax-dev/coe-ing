# Tema: iteradores, generadores y evaluación diferida.

from collections.abc import Iterable, Iterator
from itertools import accumulate, chain, islice


def scores_above(scores: Iterable[int], threshold: int) -> Iterator[int]:
    for score in scores:
        print("Inspecting score:", score)
        if score >= threshold:
            # yield entrega un resultado y suspende la función hasta la siguiente solicitud.
            yield score


def main() -> None:
    scores = [60, 85, 92, 78]
    selected = scores_above(scores, 80)
    print("Generator created; no scores inspected yet.")
    # next inicia el recorrido; convertir a lista consume solo lo que queda.
    print("First result:", next(selected))
    print("Remaining results:", list(selected))
    print("Consumed iterator:", list(selected))

    # islice limita el consumo: los elementos posteriores no llegan a inspeccionarse.
    print("First two values:", list(islice(scores_above(scores, 0), 2)))
    # chain conecta fuentes y accumulate produce subtotales sin construir listas intermedias.
    combined = chain([10, 20], [30, 40])
    print("Running totals:", list(accumulate(combined)))


if __name__ == "__main__":
    main()
