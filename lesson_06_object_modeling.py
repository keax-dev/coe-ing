# Tema: modelado con clases, dataclasses, composición, encapsulación y métodos especiales.

from abc import ABC, abstractmethod
from dataclasses import FrozenInstanceError, dataclass, replace
from decimal import Decimal

from expense_tracker.models import Expense
from expense_tracker.sample_data import sample_expenses
from expense_tracker.services import Ledger


class BudgetPolicy(ABC):
    # La clase abstracta exige que cada política implemente la decisión de aceptación.
    @abstractmethod
    def accepts(self, expense: Expense, balance: Decimal) -> bool:
        raise NotImplementedError


class StrictBudgetPolicy(BudgetPolicy):
    def accepts(self, expense: Expense, balance: Decimal) -> bool:
        return expense.amount <= balance


@dataclass
class ExpenseApplication:
    # La aplicación compone un registro y una política; cada objeto conserva su responsabilidad.
    ledger: Ledger
    policy: BudgetPolicy

    def register(self, expense: Expense) -> bool:
        # Validamos la política antes de modificar el registro.
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
    # Ledger implementa __iter__; print usa el __str__ del modelo Expense.
    for expense in app.ledger:
        print(expense)

    # replace crea otro objeto porque los modelos originales son inmutables.
    corrected_expense = replace(expenses[0], description="Team lunch")
    print("Replacement description:", corrected_expense.description)
    print("Original description:", expenses[0].description)
    try:
        # El intento falla de forma controlada para mostrar la protección de frozen=True.
        setattr(expenses[0], "description", "Changed")
    except FrozenInstanceError as error:
        print("Immutable model:", error)


if __name__ == "__main__":
    main()
