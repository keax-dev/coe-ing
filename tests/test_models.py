# Comprobamos reglas monetarias, normalización y validaciones del modelo.

from dataclasses import FrozenInstanceError, replace
from datetime import date
from decimal import Decimal

import pytest

from expense_tracker.errors import ExpenseValidationError
from expense_tracker.models import Category, Expense, create_expense, format_money, parse_money


@pytest.mark.parametrize("raw", ["12.50", "12.5", "1.000", Decimal("12.50")])
def test_money_preserves_exact_cents(raw: str | Decimal) -> None:
    amount = parse_money(raw)
    assert amount == Decimal(raw)
    assert amount.as_tuple().exponent == -2


@pytest.mark.parametrize("raw", ["", "text", "0", "-1", "1.001", "NaN", "Infinity"])
def test_invalid_money_is_rejected(raw: str) -> None:
    with pytest.raises(ExpenseValidationError):
        parse_money(raw)


def test_format_negative_balance() -> None:
    assert format_money(Decimal("-2.50")) == "-$2.50"


def test_create_expense_normalizes_user_input() -> None:
    expense = create_expense(" Team lunch ", "12.50", " FOOD ", date(2026, 10, 1))
    assert expense.description == "Team lunch"
    assert expense.category is Category.FOOD
    assert expense.spent_on == date(2026, 10, 1)


@pytest.mark.parametrize("description, category", [(" ", "food"), ("Lunch", "unknown")])
def test_invalid_expense_is_rejected(description: str, category: str) -> None:
    with pytest.raises(ExpenseValidationError):
        create_expense(description, "1.00", category)


def test_expense_is_immutable(expenses: list[Expense]) -> None:
    with pytest.raises(FrozenInstanceError):
        setattr(expenses[0], "description", "Changed")
    corrected = replace(expenses[0], description="Team lunch")
    assert expenses[0].description == "Lunch"
    assert corrected.description == "Team lunch"
