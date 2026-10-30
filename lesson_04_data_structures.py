# Tema: estructuras de datos, pilas, colas, prioridades y grafos.

from collections import deque
from heapq import heappop, heappush


def shortest_path(
    graph: dict[str, list[str]], start: str, target: str
) -> list[str] | None:
    # Una cola procesa primero las rutas más cortas en un grafo sin pesos.
    pending = deque([(start, [start])])
    visited = {start}
    while pending:
        node, path = pending.popleft()
        if node == target:
            return path
        for neighbor in graph.get(node, []):
            # El conjunto evita recorrer ciclos o visitar el mismo nodo varias veces.
            if neighbor not in visited:
                visited.add(neighbor)
                pending.append((neighbor, [*path, neighbor]))
    return None


def main() -> None:
    # Una pila es LIFO: la última acción registrada es la primera que se deshace.
    history = []
    history.append("Open document")
    history.append("Edit title")
    print("Undo last action:", history.pop())
    print("Pending history:", history)

    # Una cola es FIFO: deque permite retirar por el frente sin desplazar el resto de elementos.
    pending_jobs = deque(["Generate report", "Send notification"])
    pending_jobs.append("Create backup")
    print("Next queued job:", pending_jobs.popleft())

    # Un heap entrega la menor prioridad numérica; el contador resuelve empates por orden de llegada.
    priority_jobs = []
    for order, (priority, name) in enumerate(
        [(3, "Backup"), (1, "Alert"), (1, "Report")]
    ):
        heappush(priority_jobs, (priority, order, name))
    while priority_jobs:
        priority, _, name = heappop(priority_jobs)
        print("Priority job:", priority, name)

    # El diccionario representa vecinos y las listas representan las conexiones de cada nodo.
    graph = {
        "entry": ["library", "lab"],
        "library": ["entry", "exit"],
        "lab": ["library"],
        "exit": [],
    }
    print("Shortest route:", shortest_path(graph, "entry", "exit"))
    print("Unavailable route:", shortest_path(graph, "entry", "unknown"))


if __name__ == "__main__":
    main()
