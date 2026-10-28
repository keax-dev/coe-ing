# Tema: búsqueda secuencial, filtros y ordenamiento por una clave.
# Buscaremos gastos por descripción y los ordenaremos por monto.
# Una búsqueda secuencial revisa los elementos hasta encontrar una coincidencia.
# sorted() devuelve otra lista; list.sort() modifica la lista existente.
# La lista devuelta por sorted() conserva referencias a los mismos diccionarios.
# Ejecuta: py lesson_18_searching_and_sorting.py

from lesson_10_functions import create_expense, format_money


def find_expense(expenses, description):
    normalized_description = description.strip().casefold()
    for expense in expenses:
        if expense["description"].casefold() == normalized_description:
            return expense
    return None


def filter_expenses(expenses, query):
    normalized_query = query.strip().casefold()
    if not normalized_query:
        return []
    return [expense for expense in expenses if normalized_query in expense["description"].casefold()]


def get_amount(expense):
    # sorted llama a esta función para obtener el valor por el que debe comparar.
    return expense["amount_cents"]


if __name__ == "__main__":
    expenses = [
        create_expense("Lunch", 1250, "food"),
        create_expense("Bus", 300, "transport"),
        create_expense("Coffee", 250, "food"),
    ]
    print("Exact match:", find_expense(expenses, " BUS "))
    print("Missing match:", find_expense(expenses, "Rent"))
    print("Partial matches:", filter_expenses(expenses, "cof"))

    ordered_expenses = sorted(expenses, key=get_amount, reverse=True)
    for expense in ordered_expenses:
        print(expense["description"], format_money(expense["amount_cents"]))
    print("Original first expense:", expenses[0]["description"])

    expenses.sort(key=get_amount)
    print("Original first expense after in-place sort:", expenses[0]["description"])
