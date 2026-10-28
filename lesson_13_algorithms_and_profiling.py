# Tema: búsqueda, índices, recursividad y medición de rendimiento.

import cProfile
import pstats
from dataclasses import dataclass
from timeit import timeit


def find_score(scores: list[tuple[str, int]], name: str) -> int | None:
    # La búsqueda secuencial puede revisar toda la lista: tiempo O(n).
    for student, score in scores:
        if student == name:
            return score
    return None


@dataclass(frozen=True)
class Folder:
    name: str
    file_count: int = 0
    children: tuple["Folder", ...] = ()


def count_files(folder: Folder) -> int:
    # El caso base evita seguir descendiendo cuando el nodo no tiene hijos.
    if not folder.children:
        return folder.file_count
    # Cada llamada resuelve un subárbol; la pila crece según la profundidad.
    return folder.file_count + sum(count_files(child) for child in folder.children)


def main() -> None:
    scores = [(f"student-{number}", number % 101) for number in range(2000)]
    target = scores[-1][0]
    # Crear el índice cuesta O(n) en tiempo y memoria; las consultas son O(1) en promedio.
    index = dict(scores)
    print("Equivalent search results:", find_score(scores, target) == index.get(target))
    print("Missing result:", find_score(scores, "missing"))

    # Medimos también la construcción: preparar un índice puede no compensar para una consulta.
    print(
        "100 sequential queries (seconds):",
        timeit(lambda: find_score(scores, target), number=100),
    )
    print(
        "100 indexed queries (seconds):", timeit(lambda: index.get(target), number=100)
    )
    print("100 index builds (seconds):", timeit(lambda: dict(scores), number=100))
    tree = Folder(
        "root", 1, (Folder("images", 3), Folder("docs", 2, (Folder("drafts", 4),)))
    )
    print("Recursive file count:", count_files(tree))

    # cProfile muestra qué funciones participaron y su tiempo observado, no una garantía de velocidad.
    profiler = cProfile.Profile()
    profiler.runcall(find_score, scores, target)
    pstats.Stats(profiler).sort_stats("cumulative").print_stats(5)


if __name__ == "__main__":
    main()
