# Tema: colecciones, referencias, copias, desempaquetado y comprensiones.

from collections import Counter, defaultdict
from copy import deepcopy
from decimal import Decimal

from expense_tracker.models import Category
from expense_tracker.sample_data import sample_expenses


def main() -> None:
    records = [{"description": "Lunch", "tags": ["work"]}]
    # La asignación comparte la lista; copy solo copia el nivel exterior.
    alias = records
    shallow_copy = records.copy()
    # deepcopy también independiza los diccionarios y las listas interiores.
    deep_copy = deepcopy(records)
    shallow_copy[0]["tags"].append("food")
    print("Alias has same identity:", alias is records)
    print("Shallow copy shares nested tags:", records[0]["tags"])
    print("Deep copy keeps independent tags:", deep_copy[0]["tags"])

    expenses = sample_expenses()
    # El asterisco reúne en una lista los elementos que quedan entre el primero y el último.
    first, *middle, last = expenses
    print("Unpacked endpoints:", first.description, last.description)
    print("Unpacked middle count:", len(middle))
    # La comprensión filtra y transforma; las llaves crean un conjunto sin duplicados.
    descriptions = {expense.description for expense in expenses if expense.amount >= Decimal("3")}
    counts = Counter(expense.category.value for expense in expenses)
    # Cada categoría nueva recibe automáticamente su propia lista vacía.
    grouped: dict[Category, list[str]] = defaultdict(list)
    for expense in expenses:
        grouped[expense.category].append(expense.description)
    print("Selected descriptions:", sorted(descriptions))
    print("Category counts:", dict(counts))
    print("Grouped descriptions:", dict(grouped))


if __name__ == "__main__":
    main()
