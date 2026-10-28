# Tema: iterables, iteradores, generadores y evaluación diferida.
# yield entrega un elemento y suspende la función sin construir toda la lista.
# Un iterador se consume: recorrerlo por segunda vez ya no produce los mismos elementos.
# islice limita el consumo; chain combina fuentes sin concatenarlas en memoria.
# Ejecuta: .\.venv\Scripts\python.exe lesson_05_iterators_and_generators.py

from collections.abc import Iterable, Iterator
from decimal import Decimal
from itertools import accumulate, chain, islice

from expense_tracker.models import Expense
from expense_tracker.sample_data import sample_expenses


def expenses_above(expenses: Iterable[Expense], threshold: Decimal) -> Iterator[Expense]:
    for expense in expenses:
        print("Inspecting:", expense.description)
        if expense.amount >= threshold:
            yield expense


def main() -> None:
    expenses = sample_expenses()
    selected = expenses_above(expenses, Decimal("3.00"))
    print("Generator created; no records inspected yet.")
    print("First result:", next(selected).description)
    print("Remaining result:", [expense.description for expense in selected])
    print("Consumed generator:", list(selected))

    limited = islice(expenses_above(expenses, Decimal("0")), 2)
    print("Limited results:", [expense.description for expense in limited])
    combined = chain(expenses[:2], expenses[2:])
    running_totals = accumulate(expense.amount for expense in combined)
    print("Running totals:", list(running_totals))


if __name__ == "__main__":
    main()
