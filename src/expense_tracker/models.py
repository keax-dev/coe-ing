# Tema: modelos inmutables y validación monetaria.

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
    # Rechazamos float para no introducir sus aproximaciones en una cantidad monetaria.
    if not isinstance(value, (str, Decimal)):
        raise ExpenseValidationError("Use text or Decimal for monetary amounts.")
    try:
        amount = Decimal(value)
        # is_finite descarta NaN e infinitos antes de comparar o redondear el valor.
        if not amount.is_finite() or amount <= 0:
            raise ExpenseValidationError("Amount must be finite and positive.")
        rounded_amount = amount.quantize(CENT)
        # Exigimos centavos exactos; no redondeamos silenciosamente una entrada del usuario.
        if amount != rounded_amount:
            raise ExpenseValidationError("Amount must have at most two decimal places.")
        return rounded_amount
    except InvalidOperation as error:
        # La excepción del dominio conserva el fallo original como causa.
        raise ExpenseValidationError("Invalid monetary amount.") from error


def format_money(amount: Decimal) -> str:
    sign = "-" if amount < 0 else ""
    return f"{sign}${abs(amount):.2f}"


@dataclass(frozen=True, slots=True)
class Expense:
    # frozen impide reasignar campos y slots define los atributos permitidos.
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
        # Durante la construcción normalizamos los campos antes de exponer el objeto inmutable.
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
    # Convertimos texto de la interfaz a tipos del dominio en un único punto de entrada.
    try:
        selected_category = Category(category.strip().lower())
    except ValueError as error:
        raise ExpenseValidationError(f"Unknown category: {category}") from error
    return Expense(description, parse_money(amount), selected_category, spent_on or date.today())
