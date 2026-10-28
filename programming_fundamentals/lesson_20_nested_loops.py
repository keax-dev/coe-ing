# Tema: bucles anidados y estructuras de datos anidadas.
# Organizaremos gastos en un diccionario de meses, categorías y listas de montos.
# Cada nivel del bucle recorre un nivel de la estructura.
# Reiniciaremos cada acumulador en el nivel correspondiente para evitar mezclar totales.
# Ejecuta: py lesson_20_nested_loops.py

from lesson_10_functions import format_money


def calculate_monthly_totals(monthly_expenses):
    totals = {}
    for month, categories in monthly_expenses.items():
        monthly_total_cents = 0
        for amounts_cents in categories.values():
            for amount_cents in amounts_cents:
                monthly_total_cents += amount_cents
        totals[month] = monthly_total_cents
    return totals


if __name__ == "__main__":
    monthly_expenses = {
        "2026-09": {"food": [1250, 250], "transport": [300, 300]},
        "2026-10": {"food": [1500], "education": [2000, 500]},
        "2026-11": {},
    }

    for month, categories in monthly_expenses.items():
        print("Month:", month)
        for category, amounts_cents in categories.items():
            category_total_cents = 0
            for index, amount_cents in enumerate(amounts_cents, start=1):
                category_total_cents += amount_cents
                print(f"  {category} expense {index}: {format_money(amount_cents)}")
            print(f"  {category} total: {format_money(category_total_cents)}")

    monthly_totals = calculate_monthly_totals(monthly_expenses)
    for month, total_cents in monthly_totals.items():
        print(f"{month} total: {format_money(total_cents)}")
    print("Grand total:", format_money(sum(monthly_totals.values())))
