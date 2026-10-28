# Tema: colecciones, referencias, copias, desempaquetado y comprensiones.
# Compararemos una referencia compartida con copias superficiales y profundas.
# Los diccionarios anidados siguen compartidos después de copiar solo la lista exterior.
# Al final agruparemos modelos inmutables usando defaultdict y Counter.
# Ejecuta: .\.venv\Scripts\python.exe lesson_02_collection_semantics.py

from collections import Counter, defaultdict
from copy import deepcopy
from decimal import Decimal

from expense_tracker.models import Category
from expense_tracker.sample_data import sample_expenses


def main() -> None:
    records = [{"description": "Lunch", "tags": ["work"]}]
    alias = records
    shallow_copy = records.copy()
    deep_copy = deepcopy(records)
    shallow_copy[0]["tags"].append("food")
    print("Alias has same identity:", alias is records)
    print("Shallow copy shares nested tags:", records[0]["tags"])
    print("Deep copy keeps independent tags:", deep_copy[0]["tags"])

    expenses = sample_expenses()
    first, *middle, last = expenses
    print("Unpacked endpoints:", first.description, last.description)
    print("Unpacked middle count:", len(middle))
    descriptions = {expense.description for expense in expenses if expense.amount >= Decimal("3")}
    counts = Counter(expense.category.value for expense in expenses)
    grouped: dict[Category, list[str]] = defaultdict(list)
    for expense in expenses:
        grouped[expense.category].append(expense.description)
    print("Selected descriptions:", sorted(descriptions))
    print("Category counts:", dict(counts))
    print("Grouped descriptions:", dict(grouped))


if __name__ == "__main__":
    main()
