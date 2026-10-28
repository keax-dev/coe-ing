# Los modelos representan reglas del negocio sin depender de archivos, SQL ni HTTP.
# Decimal recibe texto para evitar incorporar aproximaciones de float al dinero.

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal, InvalidOperation
from enum import Enum
from uuid import uuid4

from expense_tracker.errors import ExpenseValidationError

CENT = Decimal("0.01")


class Category(str, Enum):
    FOOD = "food"
    TRANSPORT = "transport"
    EDUCATION = "education"
    OTHER = "other"


def parse_money(value: str | Decimal) -> Decimal:
    if not isinstance(value, (str, Decimal)):
        raise ExpenseValidationError("Use text or Decimal for monetary amounts.")
    try:
        amount = Decimal(value)
        if not amount.is_finite() or amount <= 0:
            raise ExpenseValidationError("Amount must be finite and positive.")
        rounded_amount = amount.quantize(CENT)
        if amount != rounded_amount:
            raise ExpenseValidationError("Amount must have at most two decimal places.")
        return rounded_amount
    except InvalidOperation as error:
        raise ExpenseValidationError("Invalid monetary amount.") from error


def format_money(amount: Decimal) -> str:
    sign = "-" if amount < 0 else ""
    return f"{sign}${abs(amount):.2f}"


@dataclass(frozen=True, slots=True)
class Expense:
    description: str
    amount: Decimal
    category: Category
    spent_on: date
    expense_id: str = field(default_factory=lambda: uuid4().hex)

    def __post_init__(self) -> None:
        if not self.description.strip():
            raise ExpenseValidationError("Description cannot be empty.")
        if not isinstance(self.category, Category):
            raise ExpenseValidationError("Category must be a Category member.")
        if type(self.spent_on) is not date:
            raise ExpenseValidationError("Expense date must be a date value.")
        if not self.expense_id.strip():
            raise ExpenseValidationError("Expense ID cannot be empty.")
        object.__setattr__(self, "description", self.description.strip())
        object.__setattr__(self, "amount", parse_money(self.amount))

    def __str__(self) -> str:
        return f"{self.spent_on} | {self.description} | {self.category.value} | {format_money(self.amount)}"


def create_expense(
    description: str,
    amount: str,
    category: str = "other",
    spent_on: date | None = None,
) -> Expense:
    try:
        selected_category = Category(category.strip().lower())
    except ValueError as error:
        raise ExpenseValidationError(f"Unknown category: {category}") from error
    return Expense(description, parse_money(amount), selected_category, spent_on or date.today())
