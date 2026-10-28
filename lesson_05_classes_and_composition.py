# Tema: dataclasses, composición, encapsulación, polimorfismo y métodos especiales.

from abc import ABC, abstractmethod
from collections.abc import Iterator
from dataclasses import FrozenInstanceError, dataclass, field, replace
from decimal import Decimal
from enum import Enum


class Category(str, Enum):
    BOOK = "book"
    ACCESSORY = "accessory"


@dataclass(frozen=True, slots=True)
class Product:
    name: str
    price: Decimal
    category: Category

    def __post_init__(self) -> None:
        # Validamos al construir para evitar objetos con un estado inválido.
        if not self.name.strip() or not self.price.is_finite() or self.price <= 0:
            raise ValueError("Product requires a name and a positive finite price.")

    def __str__(self) -> str:
        return f"{self.name}: ${self.price:.2f}"


class DiscountPolicy(ABC):
    @abstractmethod
    def apply(self, total: Decimal) -> Decimal:
        raise NotImplementedError


class NoDiscount(DiscountPolicy):
    def apply(self, total: Decimal) -> Decimal:
        return total


class StudentDiscount(DiscountPolicy):
    def apply(self, total: Decimal) -> Decimal:
        return total * Decimal("0.90")


@dataclass
class Cart:
    policy: DiscountPolicy
    # default_factory crea una lista independiente para cada carrito.
    _products: list[Product] = field(default_factory=list, init=False, repr=False)

    def add(self, product: Product) -> None:
        self._products.append(product)

    @property
    def total(self) -> Decimal:
        # Componemos productos y una política; cada objeto mantiene su responsabilidad.
        subtotal = sum((product.price for product in self._products), Decimal("0"))
        return self.policy.apply(subtotal)

    def __len__(self) -> int:
        return len(self._products)

    def __iter__(self) -> Iterator[Product]:
        return iter(tuple(self._products))


def main() -> None:
    book = Product("Python book", Decimal("20.00"), Category.BOOK)
    # La misma clase cambia su comportamiento al recibir otra implementación de la política.
    for policy in [NoDiscount(), StudentDiscount()]:
        cart = Cart(policy)
        cart.add(book)
        print(type(policy).__name__, "count:", len(cart), "total:", cart.total)
        for product in cart:
            print(product)
    print("Independent replacement:", replace(book, name="Advanced Python book"))
    try:
        # frozen impide cambiar campos; replace permite crear una variante independiente.
        setattr(book, "name", "Changed")
    except FrozenInstanceError:
        print("Product fields are immutable.")


if __name__ == "__main__":
    main()
