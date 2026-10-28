# Tema: mutabilidad, referencias y copias superficiales y profundas.
# Asignar una lista a otro nombre no crea una nueva lista.
# Una copia superficial crea otra lista, pero comparte los diccionarios interiores.
# deepcopy también copia las estructuras anidadas de estos datos.
# Compararemos identidad con is y contenido con ==.
# Ejecuta: py lesson_17_references_and_copies.py

from copy import deepcopy

from lesson_10_functions import create_expense


if __name__ == "__main__":
    expenses = [create_expense("Lunch", 1250, "food")]
    shared_expenses = expenses
    shared_expenses.append(create_expense("Bus", 300, "transport"))
    print("Same list:", shared_expenses is expenses)
    print("Original count after shared append:", len(expenses))

    shallow_copy = expenses.copy()
    print("Copy is a different list:", shallow_copy is not expenses)
    print("First dictionary is shared:", shallow_copy[0] is expenses[0])
    shallow_copy[0]["description"] = "Dinner"
    print("Original description after shallow edit:", expenses[0]["description"])

    shallow_copy.append(create_expense("Book", 2000, "education"))
    print("Original count after copied append:", len(expenses))
    print("Shallow copy count:", len(shallow_copy))

    backup_expenses = deepcopy(expenses)
    print("Deep copy has equal content:", backup_expenses == expenses)
    backup_expenses[0]["description"] = "Breakfast"
    print("Backup description:", backup_expenses[0]["description"])
    print("Original description:", expenses[0]["description"])

    # Los enteros son inmutables: += asocia este nombre a otro valor.
    budget_cents = 5000
    previous_budget_cents = budget_cents
    budget_cents += 1000
    print("Previous budget:", previous_budget_cents)
    print("Current budget:", budget_cents)
