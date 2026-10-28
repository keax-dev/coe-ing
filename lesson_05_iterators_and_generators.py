# Tema: iterables, iteradores, generadores y evaluación diferida.

from collections.abc import Iterable, Iterator
from decimal import Decimal
from itertools import accumulate, chain, islice

from expense_tracker.models import Expense
from expense_tracker.sample_data import sample_expenses


def expenses_above(expenses: Iterable[Expense], threshold: Decimal) -> Iterator[Expense]:
    for expense in expenses:
        print("Inspecting:", expense.description)
        if expense.amount >= threshold:
            # yield suspende aquí la función hasta que el consumidor solicite otro elemento.
            yield expense


def main() -> None:
    expenses = sample_expenses()
    # Crear el generador no ejecuta su cuerpo; next solicita el primer resultado.
    selected = expenses_above(expenses, Decimal("3.00"))
    print("Generator created; no records inspected yet.")
    print("First result:", next(selected).description)
    # Este recorrido consume lo que queda; el siguiente encontrará el iterador agotado.
    print("Remaining result:", [expense.description for expense in selected])
    print("Consumed generator:", list(selected))

    # islice consume solo dos resultados, sin evaluar el resto del generador.
    limited = islice(expenses_above(expenses, Decimal("0")), 2)
    print("Limited results:", [expense.description for expense in limited])
    # chain enlaza fuentes y accumulate entrega los subtotales sucesivos.
    combined = chain(expenses[:2], expenses[2:])
    running_totals = accumulate(expense.amount for expense in combined)
    print("Running totals:", list(running_totals))


if __name__ == "__main__":
    main()
