# Tema: arreglos y colecciones, mutabilidad, copias y comprensiones.

from array import array
from copy import deepcopy


def main() -> None:
    # array guarda valores numéricos de un mismo tipo; las listas permiten elementos heterogéneos.
    numeric_scores = array("i", [85, 92, 78])
    numeric_scores.append(90)
    print("Numeric array:", numeric_scores.tolist())
    # Una tupla conserva la forma de un registro y no permite reasignar sus posiciones.
    student = ("Alex", 85)
    print("Tuple record:", student)
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

    # Cada fila tiene su propia lista; repetir la misma fila con * compartiría sus referencias.
    matrix = [[0 for _ in range(3)] for _ in range(2)]
    matrix[0][1] = 7
    print("Independent matrix rows:", matrix)


if __name__ == "__main__":
    main()
