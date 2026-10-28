# Tema: decisiones con if, elif y else.
# Clasificaremos un gasto y determinaremos si cabe en el presupuesto.
# Solo se ejecuta la primera rama cuya condición sea verdadera.
# Ejecuta: python lesson_05_conditionals.py

if __name__ == "__main__":
    amount_cents = 1250
    remaining_cents = 5000
    category = "food"

    if amount_cents <= 0:
        print("Invalid expense: amount must be positive.")
    elif amount_cents > remaining_cents:
        print("Expense exceeds the remaining budget.")
    elif amount_cents == remaining_cents:
        print("Expense uses the entire remaining budget.")
    else:
        print("Expense accepted.")
        remaining_cents -= amount_cents
        print("Remaining cents:", remaining_cents)

    if category == "food":
        print("Review your food spending each week.")
    elif category == "transport":
        print("Compare your transport options.")
    else:
        print("Review this category each month.")

# Práctica:
# 1. Prueba montos negativos, cero, iguales al saldo y superiores al saldo.
# 2. Agrega una categoría entertainment con su propio mensaje.
# 3. Agrega un aviso cuando el saldo final sea menor que 1000 centavos.
