# Tema: búsqueda, recursividad, complejidad y medición de rendimiento.
# La búsqueda secuencial cuesta O(n); construir un índice cuesta O(n) y permite
# consultas promedio O(1). El índice también ocupa memoria adicional O(n).
# La recursividad necesita un caso base y consume pila según la profundidad del árbol.
# Medimos construcción y consultas por separado; un índice no siempre compensa para una consulta.
# Ejecuta: .\.venv\Scripts\python.exe lesson_14_algorithms_and_profiling.py

import cProfile
import pstats
from dataclasses import dataclass, replace
from decimal import Decimal
from timeit import timeit

from expense_tracker.models import Expense
from expense_tracker.sample_data import sample_expenses


def find_sequential(expenses: list[Expense], expense_id: str) -> Expense | None:
    for expense in expenses:
        if expense.expense_id == expense_id:
            return expense
    return None


@dataclass(frozen=True)
class BudgetNode:
    name: str
    amount: Decimal = Decimal("0.00")
    children: tuple["BudgetNode", ...] = ()


def recursive_total(node: BudgetNode) -> Decimal:
    # Un nodo sin hijos es el caso base: su subtotal es su propio monto.
    if not node.children:
        return node.amount
    return node.amount + sum((recursive_total(child) for child in node.children), Decimal("0"))


def main() -> None:
    template = sample_expenses()[0]
    expenses = [replace(template, expense_id=f"expense-{index}") for index in range(2000)]
    target_id = expenses[-1].expense_id
    index_by_id = {expense.expense_id: expense for expense in expenses}
    print("Same result:", find_sequential(expenses, target_id) == index_by_id.get(target_id))
    print(
        "100 sequential queries (seconds):",
        timeit(lambda: find_sequential(expenses, target_id), number=100),
    )
    print("100 indexed queries (seconds):", timeit(lambda: index_by_id.get(target_id), number=100))
    print(
        "100 index builds (seconds):",
        timeit(lambda: {item.expense_id: item for item in expenses}, number=100),
    )

    tree = BudgetNode(
        "all",
        children=(
            BudgetNode("food", children=(BudgetNode("lunch", Decimal("12.50")),)),
            BudgetNode("transport", Decimal("3.00")),
        ),
    )
    print("Recursive total:", recursive_total(tree))
    profiler = cProfile.Profile()
    profiler.runcall(find_sequential, expenses, target_id)
    pstats.Stats(profiler).sort_stats("cumulative").print_stats(5)


if __name__ == "__main__":
    main()
