# Tema: funciones, parámetros, valores de retorno y alcance de variables.
# Extraeremos operaciones del registro para reutilizarlas sin copiar código.
# return entrega un resultado; print solo lo muestra en pantalla.
# Las variables creadas dentro de una función son locales a esa función.
# Ejecuta: python lesson_10_functions.py


def format_money(amount_cents):
    # Separamos el signo para que también se muestren correctamente los saldos negativos.
    sign = "-" if amount_cents < 0 else ""
    absolute_cents = abs(amount_cents)
    return f"{sign}${absolute_cents // 100}.{absolute_cents % 100:02d}"


def create_expense(description, amount_cents, category="other"):
    return {
        "description": description.strip(),
        "amount_cents": amount_cents,
        "category": category.strip().lower(),
    }


def calculate_total(expenses):
    total_cents = 0
    for expense in expenses:
        total_cents += expense["amount_cents"]
    return total_cents


def calculate_balance(budget_cents, expenses):
    return budget_cents - calculate_total(expenses)


if __name__ == "__main__":
    expenses = [
        create_expense("Lunch", 1250, "food"),
        create_expense("Notebook", 400),
    ]
    total_cents = calculate_total(expenses)
    print("Total:", format_money(total_cents))
    print("Balance:", format_money(calculate_balance(5000, expenses)))
    print("Keyword arguments:", create_expense(amount_cents=300, description="Bus"))

# Práctica:
# 1. Crea una función que devuelva el gasto más alto; decide qué devolver si no hay gastos.
# 2. Crea una función que filtre gastos por categoría.
# 3. Cambia el presupuesto pasado a calculate_balance sin modificar la función.
