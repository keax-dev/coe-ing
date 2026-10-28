# Tema: anotaciones, uniones, genéricos, TypedDict y protocolos estructurales.

from collections.abc import Sequence
from typing import Protocol, TypedDict, TypeVar

Item = TypeVar("Item")


def first_or_none(items: Sequence[Item]) -> Item | None:
    # El tipo de los elementos se conserva en el resultado; None representa una secuencia vacía.
    return items[0] if items else None


class ScoreReader(Protocol):
    def read(self) -> list[int]: ...


class MemoryReader:
    # No necesita heredar de ScoreReader: implementar el método requerido cumple el contrato.
    def read(self) -> list[int]:
        return [85, 92, 78]


class Summary(TypedDict):
    count: int
    average: float | None


def summarize(reader: ScoreReader) -> Summary:
    scores = reader.read()
    # TypedDict documenta claves y tipos para el analizador; no valida valores al ejecutar.
    return {
        "count": len(scores),
        "average": sum(scores) / len(scores) if scores else None,
    }


def main() -> None:
    print("First name:", first_or_none(["Alex", "Sam"]))
    print("Empty result:", first_or_none([]))
    print("Typed summary:", summarize(MemoryReader()))


if __name__ == "__main__":
    main()
