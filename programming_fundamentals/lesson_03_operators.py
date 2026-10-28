# Tema: operadores y expresiones.
# Calcularemos el saldo, compararemos gastos y combinaremos condiciones.
# = asigna un valor; == compara valores. Los paréntesis aclaran la precedencia.
# Ejecuta: python lesson_03_operators.py

if __name__ == "__main__":
    budget_cents = 10000
    lunch_cents = 1250
    transport_cents = 300
    total_cents = lunch_cents + transport_cents
    remaining_cents = budget_cents - total_cents

    print("Total cents:", total_cents)
    print("Remaining cents:", remaining_cents)
    print("Weekly transport cents:", transport_cents * 5)
    print("Budget used (%):", total_cents / budget_cents * 100)
    print("Whole dollars:", total_cents // 100)
    print("Remaining cents after whole dollars:", total_cents % 100)
    print("Squared value:", 3 ** 2)

    is_over_budget = total_cents > budget_cents
    print("Exactly on budget:", total_cents == budget_cents)
    print("Within budget:", total_cents <= budget_cents)
    print("Valid and affordable:", lunch_cents > 0 and not is_over_budget)
    print("Needs review:", lunch_cents > 5000 or is_over_budget)

    total_cents += 200
    print("Total after service fee:", total_cents)
    print("Grouped expression:", (lunch_cents + transport_cents) * 2)
    print("Default precedence:", lunch_cents + transport_cents * 2)
    print("Known category:", "food" in ["food", "transport"])

# Práctica:
# 1. Agrega un tercer gasto y actualiza el saldo.
# 2. Comprueba si el saldo está entre 0 y 5000 usando comparaciones.
# 3. Distribuye 1000 centavos entre tres personas con // y %.
