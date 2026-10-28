# Tema: listas, tuplas, diccionarios, conjuntos y comprensiones.
# Representaremos cada gasto con un diccionario y el registro con una lista.
# Una tupla agrupa valores que no modificaremos; un conjunto elimina duplicados.
# Una comprensión construye una colección a partir de otra, con un filtro opcional.
# Ejecuta: python lesson_08_collections.py

if __name__ == "__main__":
    allowed_categories = ("food", "transport", "education")
    expenses = [
        {"description": "Lunch", "amount_cents": 1250, "category": "food"},
        {"description": "Bus", "amount_cents": 300, "category": "transport"},
    ]
    expenses.append({"description": "Coffee", "amount_cents": 250, "category": "food"})

    print("First expense:", expenses[0])
    print("Last description:", expenses[-1]["description"])
    print("First two expenses:", expenses[:2])
    print("Expense count:", len(expenses))

    expenses[0]["amount_cents"] = 1300
    print("Optional note:", expenses[0].get("note", "No note"))
    for key, value in expenses[0].items():
        print(key, "=", value)

    used_categories = {expense["category"] for expense in expenses}
    food_expenses = [expense for expense in expenses if expense["category"] == "food"]
    amounts_cents = [expense["amount_cents"] for expense in expenses]

    print("Allowed categories:", allowed_categories)
    print("Used categories:", sorted(used_categories))
    print("Food expenses:", food_expenses)
    print("Total cents:", sum(amounts_cents))
    removed_expense = expenses.pop()
    print("Removed expense:", removed_expense)

# Práctica:
# 1. Agrega un gasto de educación y comprueba las categorías únicas.
# 2. Construye una lista con gastos superiores a 500 centavos.
# 3. Agrega una clave note a un gasto y consulta su valor con get().
