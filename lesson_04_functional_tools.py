# Tema: lambda, funciones de orden superior, map, filter, reduce, any, all y zip.
# Una lambda devuelve una expresión; def conviene cuando hay varios pasos o reglas.
# Las funciones de orden superior reciben o devuelven otras funciones.
# map y filter producen iteradores: aquí los convertimos para inspeccionar su contenido.
# Compararemos estas herramientas con una comprensión de listas equivalente.
# Ejecuta: .\.venv\Scripts\python.exe lesson_04_functional_tools.py

from collections.abc import Callable, Iterable
from decimal import Decimal
from functools import partial, reduce

from expense_tracker.models import Category, Expense
from expense_tracker.sample_data import sample_expenses
from expense_tracker.services import filter_expenses


def select_expenses(
    expenses: Iterable[Expense], predicate: Callable[[Expense], bool]
) -> list[Expense]:
    return [expense for expense in expenses if predicate(expense)]


def main() -> None:
    expenses = sample_expenses()
    ordered = sorted(expenses, key=lambda expense: expense.amount, reverse=True)
    names = list(map(lambda expense: expense.description.upper(), expenses))
    food = list(filter(lambda expense: expense.category == Category.FOOD, expenses))
    food_comprehension = [expense for expense in expenses if expense.category == Category.FOOD]
    total = reduce(
        lambda accumulated, expense: accumulated + expense.amount, expenses, Decimal("0")
    )
    select_food = partial(filter_expenses, category=Category.FOOD)

    print("Ordered descriptions:", [expense.description for expense in ordered])
    print("Mapped descriptions:", names)
    print("Equivalent filters:", food == food_comprehension == select_food(expenses))
    print("Reduced total:", total)
    print("Any expensive expense:", any(expense.amount >= Decimal("20") for expense in expenses))
    print("All expenses positive:", all(expense.amount > 0 for expense in expenses))
    print("Selected count:", len(select_expenses(expenses, lambda expense: expense.amount < 5)))
    # strict evita perder datos silenciosamente si las colecciones tienen distinto tamaño.
    for number, (name, expense) in enumerate(zip(names, expenses, strict=True), start=1):
        print(number, name, expense.amount)


if __name__ == "__main__":
    main()
