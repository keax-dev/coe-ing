# Tema: patrón Strategy para intercambiar algoritmos de cálculo de envío.

from abc import ABC, abstractmethod


class ShippingStrategy(ABC):
    @abstractmethod
    def calculate_cost(self, weight: int) -> int:
        raise NotImplementedError


class StandardShipping(ShippingStrategy):
    def calculate_cost(self, weight: int) -> int:
        return weight * 2


class ExpressShipping(ShippingStrategy):
    def calculate_cost(self, weight: int) -> int:
        return weight * 4


class ShippingCalculator:
    def __init__(self, strategy: ShippingStrategy) -> None:
        # El contexto recibe el algoritmo; no necesita decidir cómo funciona cada alternativa.
        self.strategy = strategy

    def calculate(self, weight: int) -> int:
        return self.strategy.calculate_cost(weight)


def main() -> None:
    calculator = ShippingCalculator(StandardShipping())
    print("Standard shipping cost:", calculator.calculate(3))

    # Cambiamos el algoritmo en ejecución sin modificar el código del contexto.
    calculator.strategy = ExpressShipping()
    print("Express shipping cost:", calculator.calculate(3))


if __name__ == "__main__":
    main()
