# Tema: diseño de algoritmos y división de un problema en pasos.
# Resolveremos la decisión de aceptar o rechazar un gasto antes de guardarlo.
# Entrada: presupuesto, gastos actuales y un monto nuevo.
# Procesamiento: validar el monto, sumar gastos y calcular el saldo disponible.
# Salida: una decisión y el saldo que quedaría; la lista original no se modifica.
# Pseudocódigo: validar -> calcular saldo -> comparar -> devolver resultado.
# Esta política rechaza gastos superiores al saldo; es distinta del aviso de la lección 14.
# Ejecuta: py lesson_15_algorithm_design.py

from lesson_10_functions import calculate_balance, create_expense, format_money


def evaluate_expense(budget_cents, expenses, amount_cents):
    if type(amount_cents) is not int or amount_cents <= 0:
        raise ValueError("Amount must be a positive integer in cents.")

    available_cents = calculate_balance(budget_cents, expenses)
    if amount_cents > available_cents:
        return {"accepted": False, "balance_cents": available_cents}
    return {"accepted": True, "balance_cents": available_cents - amount_cents}


if __name__ == "__main__":
    expenses = [create_expense("Lunch", 1250, "food")]
    budget_cents = 2000

    # Probamos un gasto menor, igual y mayor que el saldo disponible.
    # Los escenarios son independientes: evaluar no registra el gasto.
    for amount_cents in [300, 750, 1000]:
        result = evaluate_expense(budget_cents, expenses, amount_cents)
        print("Requested amount:", format_money(amount_cents))
        print("Accepted:", result["accepted"])
        print("Resulting balance:", format_money(result["balance_cents"]))

    print("Recorded expenses:", len(expenses))
