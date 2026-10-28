# Verificamos resultados de negocio, casos vacíos y aislamiento entre registros.

from decimal import Decimal

import pytest

from expense_tracker.errors import ExpenseValidationError
from expense_tracker.models import Category, Expense
from expense_tracker.services import Ledger, filter_expenses, total_amount, totals_by_category


def test_known_total_and_empty_total(expenses: list[Expense]) -> None:
    assert total_amount(expenses) == Decimal("38.00")
    assert total_amount(iter(expenses)) == Decimal("38.00")
    assert total_amount([]) == Decimal("0.00")


def test_filter_does_not_mutate_original(expenses: list[Expense]) -> None:
    original = expenses.copy()
    selected = filter_expenses(expenses, category=Category.FOOD, minimum=Decimal("3.00"))
    assert [expense.description for expense in selected] == ["Lunch"]
    assert expenses == original


def test_category_totals(expenses: list[Expense]) -> None:
    assert totals_by_category(expenses) == {
        Category.FOOD: Decimal("15.00"),
        Category.TRANSPORT: Decimal("3.00"),
        Category.EDUCATION: Decimal("20.00"),
    }


def test_ledger_defaults_are_independent(expenses: list[Expense]) -> None:
    first = Ledger(Decimal("10.00"))
    second = Ledger(Decimal("10.00"))
    first.add(expenses[0])
    assert len(second) == 0
    assert first.balance == Decimal("-2.50")
    assert list(first) == [expenses[0]]


def test_duplicate_id_is_rejected(expenses: list[Expense]) -> None:
    ledger = Ledger(Decimal("50.00"))
    ledger.add(expenses[0])
    with pytest.raises(ExpenseValidationError, match="already exists"):
        ledger.add(expenses[0])
    assert len(ledger) == 1
