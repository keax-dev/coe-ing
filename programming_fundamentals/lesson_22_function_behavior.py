# Tema: argumentos mutables, efectos secundarios y valores predeterminados.
# Una función puede cambiar los objetos que recibe; eso es un efecto secundario.
# Compararemos agregar a una lista existente con devolver una lista nueva.
# También veremos por qué una lista como valor predeterminado se comparte entre llamadas.
# Usar None permite crear una lista independiente cada vez que no se proporciona una.
# Ejecuta: py lesson_22_function_behavior.py

from copy import deepcopy

from lesson_10_functions import create_expense


def append_expense(expenses, expense):
    # Modifica la lista del llamador y devuelve None de forma implícita.
    expenses.append(expense)


def with_added_expense(expenses, expense):
    # Para estos diccionarios simples, deepcopy permite editar el resultado sin afectar el origen.
    updated_expenses = deepcopy(expenses)
    updated_expenses.append(deepcopy(expense))
    return updated_expenses


def collect_with_shared_default(expense, expenses=[]):
    # Este patrón es incorrecto de forma intencional: el valor se crea al definir la función.
    expenses.append(expense)
    return expenses


def collect_with_safe_default(expense, expenses=None):
    if expenses is None:
        expenses = []
    # Si el llamador proporciona una lista, esta versión también la modifica.
    expenses.append(expense)
    return expenses


if __name__ == "__main__":
    lunch = create_expense("Lunch", 1250, "food")
    bus = create_expense("Bus", 300, "transport")
    expenses = [lunch]

    updated_expenses = with_added_expense(expenses, bus)
    updated_expenses[0]["description"] = "Dinner"
    print("Original after independent update:", expenses)
    print("Independent result:", updated_expenses)

    return_value = append_expense(expenses, bus)
    print("Original after in-place update:", expenses)
    print("In-place return value:", return_value)

    first_shared = collect_with_shared_default(lunch)
    second_shared = collect_with_shared_default(bus)
    print("Default list is shared:", first_shared is second_shared)
    print("First shared result count after second call:", len(first_shared))

    first_independent = collect_with_safe_default(lunch)
    second_independent = collect_with_safe_default(bus)
    print("Safe calls use different lists:", first_independent is not second_independent)
    print("Independent counts:", len(first_independent), len(second_independent))
