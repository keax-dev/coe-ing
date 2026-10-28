# Tema: proyecto integrador de fundamentos de programación.
# Construiremos un registro de gastos con menú, validación, resúmenes y persistencia.
# Aquí se combinan variables, operadores, entrada/salida, condiciones, bucles,
# colecciones, cadenas, funciones, módulos, excepciones y archivos.
# El modo normal muestra un ejemplo completo sin modificar tus datos guardados.
# El modo interactivo guarda únicamente cuando eliges la opción de guardar.
# Ejecuta: python lesson_14_expense_tracker.py --interactive

import sys
from pathlib import Path
from tempfile import TemporaryDirectory

from lesson_10_functions import calculate_balance, calculate_total, create_expense, format_money
from lesson_12_exceptions import parse_amount
from lesson_13_files import load_expenses, save_expenses


DATA_PATH = Path(__file__).resolve().parent / "data" / "expenses.json"
DEFAULT_BUDGET_CENTS = 10000


def show_expenses(expenses):
    if not expenses:
        print("No expenses recorded.")
        return
    for index, expense in enumerate(expenses, start=1):
        print(
            f"{index}. {expense['description']} | {expense['category']} | "
            f"{format_money(expense['amount_cents'])}"
        )


def show_summary(expenses, budget_cents):
    print("Budget:", format_money(budget_cents))
    print("Total:", format_money(calculate_total(expenses)))
    balance_cents = calculate_balance(budget_cents, expenses)
    print("Balance:", format_money(balance_cents))
    if balance_cents < 0:
        print("Warning: budget exceeded.")

    totals_by_category = {}
    for expense in expenses:
        category = expense["category"]
        totals_by_category[category] = totals_by_category.get(category, 0) + expense["amount_cents"]
    for category, total_cents in sorted(totals_by_category.items()):
        print(f"{category}: {format_money(total_cents)}")


def read_expense():
    description = input("Description: ").strip()
    if not description:
        raise ValueError("Description cannot be empty.")
    amount_cents = parse_amount(input("Amount in cents: ").strip())
    category = input("Category: ").strip().lower()
    if not category:
        raise ValueError("Category cannot be empty.")
    return create_expense(description, amount_cents, category)


def run_interactive(file_path=DATA_PATH):
    expenses = []
    budget_cents = DEFAULT_BUDGET_CENTS
    print("EXPENSE TRACKER")
    print("Use option 5 to load saved records and option 4 to save changes.")
    while True:
        print("\n1. Add expense\n2. List expenses\n3. Summary\n4. Save\n5. Load\n6. Set budget\n0. Exit")
        choice = input("Choose an option: ").strip()
        try:
            if choice == "1":
                # Primero validamos; solo agregamos el gasto si todos los datos son correctos.
                expenses.append(read_expense())
                print("Expense added.")
            elif choice == "2":
                show_expenses(expenses)
            elif choice == "3":
                show_summary(expenses, budget_cents)
            elif choice == "4":
                save_expenses(expenses, file_path)
                print("Saved to:", file_path)
            elif choice == "5":
                # Si la carga falla, la asignación no ocurre y conservamos la lista actual.
                expenses = load_expenses(file_path)
                print("Loaded expenses:", len(expenses))
            elif choice == "6":
                budget_cents = parse_amount(input("Budget in cents: ").strip())
                print("Budget updated for this session.")
            elif choice == "0":
                print("Goodbye. Only explicitly saved expenses are kept.")
                break
            else:
                print("Unknown option.")
        except (ValueError, OSError) as error:
            print("Could not complete the operation:", error)


def run_demo():
    expenses = [
        create_expense("Lunch", 1250, "food"),
        create_expense("Bus", 300, "transport"),
        create_expense("Coffee", 250, "food"),
    ]
    show_expenses(expenses)
    show_summary(expenses, DEFAULT_BUDGET_CENTS)
    with TemporaryDirectory() as temporary_directory:
        file_path = Path(temporary_directory) / "expenses.json"
        save_expenses(expenses, file_path)
        restored_expenses = load_expenses(file_path)
        print("Save/load successful:", restored_expenses == expenses)


if __name__ == "__main__":
    try:
        if "--interactive" in sys.argv:
            run_interactive()
        else:
            run_demo()
    except (EOFError, KeyboardInterrupt):
        print("\nSession ended.")
