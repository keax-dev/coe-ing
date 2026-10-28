# Tema: contadores, acumuladores, promedios, máximos y mínimos.
# Calcularemos estadísticas recorriendo la lista una sola vez.
# El contador registra cuántos elementos hay; el acumulador suma sus montos.
# Si no hay gastos, el promedio, el mínimo y el máximo no están definidos.
# El promedio usa decimales solo para mostrarlo; los gastos siguen siendo centavos enteros.
# Ejecuta: py lesson_19_statistics.py

from lesson_10_functions import create_expense, format_money


def summarize_expenses(expenses):
    count = 0
    total_cents = 0
    minimum_cents = None
    maximum_cents = None

    for expense in expenses:
        amount_cents = expense["amount_cents"]
        count += 1
        total_cents += amount_cents
        if minimum_cents is None or amount_cents < minimum_cents:
            minimum_cents = amount_cents
        if maximum_cents is None or amount_cents > maximum_cents:
            maximum_cents = amount_cents

    average_cents = total_cents / count if count else None
    return {
        "count": count,
        "total_cents": total_cents,
        "average_cents": average_cents,
        "minimum_cents": minimum_cents,
        "maximum_cents": maximum_cents,
    }


if __name__ == "__main__":
    expenses = [
        create_expense("Lunch", 1250, "food"),
        create_expense("Bus", 300, "transport"),
        create_expense("Coffee", 250, "food"),
    ]
    for records in [expenses, []]:
        summary = summarize_expenses(records)
        print("Expense count:", summary["count"])
        print("Total:", format_money(summary["total_cents"]))
        if summary["count"]:
            print(f"Average: ${summary['average_cents'] / 100:.2f}")
            print("Minimum:", format_money(summary["minimum_cents"]))
            print("Maximum:", format_money(summary["maximum_cents"]))
        else:
            print("Average, minimum and maximum: unavailable")
