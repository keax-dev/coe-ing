# Tema: lambda, funciones de orden superior, map, filter, reduce, any, all y zip.

from collections.abc import Callable, Iterable
from decimal import Decimal
from functools import partial, reduce

from expense_tracker.models import Category, Expense
from expense_tracker.sample_data import sample_expenses
from expense_tracker.services import filter_expenses


def select_expenses(
    expenses: Iterable[Expense], predicate: Callable[[Expense], bool]
) -> list[Expense]:
    # La condición llega como función: el mismo recorrido admite distintas reglas de selección.
    return [expense for expense in expenses if predicate(expense)]


def main() -> None:
    expenses = sample_expenses()
    # lambda expresa una función breve que devuelve la clave de ordenamiento.
    ordered = sorted(expenses, key=lambda expense: expense.amount, reverse=True)
    # map transforma y filter selecciona; list consume sus iteradores para mostrar los resultados.
    names = list(map(lambda expense: expense.description.upper(), expenses))
    food = list(filter(lambda expense: expense.category == Category.FOOD, expenses))
    # La comprensión permite expresar el mismo filtro sin una función adicional.
    food_comprehension = [expense for expense in expenses if expense.category == Category.FOOD]
    # reduce combina cada elemento con el acumulado, empezando por cero.
    total = reduce(
        lambda accumulated, expense: accumulated + expense.amount, expenses, Decimal("0")
    )
    # partial fija un argumento y devuelve una función reutilizable con esa configuración.
    select_food = partial(filter_expenses, category=Category.FOOD)

    print("Ordered descriptions:", [expense.description for expense in ordered])
    print("Mapped descriptions:", names)
    print("Equivalent filters:", food == food_comprehension == select_food(expenses))
    print("Reduced total:", total)
    # any termina al encontrar un verdadero; all termina al encontrar un falso.
    print("Any expensive expense:", any(expense.amount >= Decimal("20") for expense in expenses))
    print("All expenses positive:", all(expense.amount > 0 for expense in expenses))
    print("Selected count:", len(select_expenses(expenses, lambda expense: expense.amount < 5)))
    # strict evita perder datos silenciosamente si las colecciones tienen distinto tamaño.
    # zip empareja las colecciones y enumerate agrega un número a cada pareja.
    for number, (name, expense) in enumerate(zip(names, expenses, strict=True), start=1):
        print(number, name, expense.amount)


if __name__ == "__main__":
    main()
