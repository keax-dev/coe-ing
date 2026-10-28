# Tema: anotaciones de tipos, Optional, TypedDict, genéricos y contratos estructurales.

from collections.abc import Sequence
from decimal import Decimal
from typing import Protocol, TypedDict, TypeVar

from expense_tracker.models import Expense
from expense_tracker.sample_data import sample_expenses
from expense_tracker.services import total_amount

Item = TypeVar("Item")


def first_or_none(items: Sequence[Item]) -> Item | None:
    # El tipo de retorno conserva el tipo de los elementos o indica ausencia con None.
    return items[0] if items else None


class ExpenseReader(Protocol):
    # El contrato describe los métodos necesarios, sin imponer una clase base concreta.
    def list_all(self) -> list[Expense]: ...


class Summary(TypedDict):
    # TypedDict describe claves y valores para mypy; no valida el diccionario al ejecutarlo.
    count: int
    total: Decimal


class SampleReader:
    # No necesita heredar de ExpenseReader: su estructura cumple el contrato.
    def list_all(self) -> list[Expense]:
        return sample_expenses()


def build_summary(reader: ExpenseReader) -> Summary:
    expenses = reader.list_all()
    return {"count": len(expenses), "total": total_amount(expenses)}


def main() -> None:
    print("Typed summary:", build_summary(SampleReader()))
    print("First expense:", first_or_none(sample_expenses()))
    print("Empty sequence:", first_or_none([]))
    # Para comprobar un error de tipos sin romper el ejemplo, cambia en tu copia
    # el valor de count por texto y ejecuta mypy sobre este archivo.


if __name__ == "__main__":
    main()
