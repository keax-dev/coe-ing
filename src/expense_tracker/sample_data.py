# Tema: datos reproducibles para demostraciones y pruebas.

from datetime import date
from decimal import Decimal

from expense_tracker.models import Category, Expense


def sample_expenses() -> list[Expense]:
    # Fechas e IDs fijos hacen reproducibles los ejemplos; cada llamada crea una lista nueva.
    return [
        Expense("Lunch", Decimal("12.50"), Category.FOOD, date(2026, 10, 1), "sample-lunch"),
        Expense("Bus", Decimal("3.00"), Category.TRANSPORT, date(2026, 10, 2), "sample-bus"),
        Expense("Coffee", Decimal("2.50"), Category.FOOD, date(2026, 10, 3), "sample-coffee"),
        Expense("Book", Decimal("20.00"), Category.EDUCATION, date(2026, 10, 4), "sample-book"),
    ]
