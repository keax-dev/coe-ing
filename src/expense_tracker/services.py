# Tema: cálculos del negocio y registro de gastos.

from collections import defaultdict
from collections.abc import Iterable, Iterator
from dataclasses import dataclass, field
from decimal import Decimal

from expense_tracker.errors import ExpenseValidationError
from expense_tracker.models import Category, Expense, parse_money


def total_amount(expenses: Iterable[Expense]) -> Decimal:
    # Iterable admite listas y generadores; el valor inicial mantiene Decimal incluso sin gastos.
    return sum((expense.amount for expense in expenses), start=Decimal("0.00"))


def totals_by_category(expenses: Iterable[Expense]) -> dict[Category, Decimal]:
    # Cada categoría que aparece por primera vez recibe un acumulador decimal en cero.
    totals: dict[Category, Decimal] = defaultdict(lambda: Decimal("0.00"))
    for expense in expenses:
        totals[expense.category] += expense.amount
    return dict(totals)


def filter_expenses(
    expenses: Iterable[Expense],
    *,
    category: Category | None = None,
    minimum: Decimal = Decimal("0.00"),
) -> list[Expense]:
    return [
        expense
        for expense in expenses
        if expense.amount >= minimum and (category is None or expense.category == category)
    ]


@dataclass
class Ledger:
    budget: Decimal
    # Cada instancia obtiene su propia lista; el constructor no permite inyectar la lista interna.
    _expenses: list[Expense] = field(default_factory=list, init=False, repr=False)

    def __post_init__(self) -> None:
        self.budget = parse_money(self.budget)

    @property
    def balance(self) -> Decimal:
        # El saldo se calcula a partir del estado actual en lugar de almacenarse por separado.
        return self.budget - total_amount(self._expenses)

    def add(self, expense: Expense) -> None:
        if any(item.expense_id == expense.expense_id for item in self._expenses):
            raise ExpenseValidationError("Expense ID already exists.")
        self._expenses.append(expense)

    def __len__(self) -> int:
        return len(self._expenses)

    def __iter__(self) -> Iterator[Expense]:
        # Iteramos sobre una instantánea para no exponer la lista interna.
        return iter(tuple(self._expenses))
