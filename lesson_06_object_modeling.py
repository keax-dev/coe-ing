# Tema: modelado con clases, dataclasses, composición, encapsulación y métodos especiales.
# Expense es un objeto de valor inmutable; Ledger compone varios gastos.
# __len__, __iter__ y __str__ permiten integrar nuestros modelos con operaciones de Python.
# La herencia se usa para expresar una relación real: una política especializada de presupuesto.
# Preferimos composición para reunir entidades que tienen responsabilidades diferentes.
# Ejecuta: .\.venv\Scripts\python.exe lesson_06_object_modeling.py

from abc import ABC, abstractmethod
from dataclasses import FrozenInstanceError, dataclass, replace
from decimal import Decimal

from expense_tracker.models import Expense
from expense_tracker.sample_data import sample_expenses
from expense_tracker.services import Ledger


class BudgetPolicy(ABC):
    @abstractmethod
    def accepts(self, expense: Expense, balance: Decimal) -> bool:
        raise NotImplementedError


class StrictBudgetPolicy(BudgetPolicy):
    def accepts(self, expense: Expense, balance: Decimal) -> bool:
        return expense.amount <= balance


@dataclass
class ExpenseApplication:
    ledger: Ledger
    policy: BudgetPolicy

    def register(self, expense: Expense) -> bool:
        if not self.policy.accepts(expense, self.ledger.balance):
            return False
        self.ledger.add(expense)
        return True


def main() -> None:
    expenses = sample_expenses()
    app = ExpenseApplication(Ledger(Decimal("15.00")), StrictBudgetPolicy())
    for expense in expenses:
        print("Accepted:", expense.description, app.register(expense))
    print("Ledger length:", len(app.ledger))
    print("Ledger balance:", app.ledger.balance)
    for expense in app.ledger:
        print(expense)

    corrected_expense = replace(expenses[0], description="Team lunch")
    print("Replacement description:", corrected_expense.description)
    print("Original description:", expenses[0].description)
    try:
        setattr(expenses[0], "description", "Changed")
    except FrozenInstanceError as error:
        print("Immutable model:", error)


if __name__ == "__main__":
    main()
