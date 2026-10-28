# Tema: referencias, copias, desempaquetado y transformaciones de colecciones.

from collections import Counter, defaultdict
from copy import deepcopy


def main() -> None:
    users = [{"name": "Alex", "tags": ["python"]}]
    alias = users
    shallow_copy = users.copy()
    deep_copy = deepcopy(users)

    # La copia superficial comparte el diccionario y su lista interior con el original.
    shallow_copy[0]["tags"].append("sql")
    print("Same list:", alias is users)
    print("Original tags:", users[0]["tags"])
    print("Independent deep copy:", deep_copy[0]["tags"])

    scores = [("Alex", 85), ("Sam", 92), ("Taylor", 78), ("Robin", 92)]
    # El asterisco reúne los elementos entre el primero y el último en una nueva lista.
    first, *middle, last = scores
    print("Unpacked endpoints:", first, last)
    print("Middle records:", middle)

    # Cada comprensión elige una estructura distinta: lista, conjunto o diccionario.
    passed_names = [name for name, score in scores if score >= 80]
    unique_scores = {score for _, score in scores}
    scores_by_name = {name: score for name, score in scores}
    print("Passed names:", passed_names)
    print("Unique scores:", sorted(unique_scores))
    print("Score lookup:", scores_by_name["Sam"])

    # Counter cuenta repeticiones y defaultdict crea una lista por cada clave nueva.
    counts = Counter(score for _, score in scores)
    grouped: dict[str, list[str]] = defaultdict(list)
    for name, score in scores:
        grouped["passed" if score >= 80 else "review"].append(name)
    print("Score frequencies:", dict(counts))
    print("Grouped students:", dict(grouped))


if __name__ == "__main__":
    main()
