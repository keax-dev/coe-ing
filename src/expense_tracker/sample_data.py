# Las demostraciones comparten datos reproducibles y no alteran registros del usuario.

from datetime import date
from decimal import Decimal

from expense_tracker.models import Category, Expense


def sample_expenses() -> list[Expense]:
    return [
        Expense("Lunch", Decimal("12.50"), Category.FOOD, date(2026, 10, 1), "sample-lunch"),
        Expense("Bus", Decimal("3.00"), Category.TRANSPORT, date(2026, 10, 2), "sample-bus"),
        Expense("Coffee", Decimal("2.50"), Category.FOOD, date(2026, 10, 3), "sample-coffee"),
        Expense("Book", Decimal("20.00"), Category.EDUCATION, date(2026, 10, 4), "sample-book"),
    ]
