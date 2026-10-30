# Tema: patrón Observer para notificar novedades a varios suscriptores.

from abc import ABC, abstractmethod


class Observer(ABC):
    @abstractmethod
    def update(self, message: str) -> None:
        raise NotImplementedError


class UserObserver(Observer):
    def __init__(self, name: str) -> None:
        self.name = name

    def update(self, message: str) -> None:
        print(f"{self.name} received: {message}")


class NewsPublisher:
    def __init__(self) -> None:
        self._observers: list[Observer] = []

    def subscribe(self, observer: Observer) -> None:
        # Evitamos registrar dos veces al mismo suscriptor.
        if observer not in self._observers:
            self._observers.append(observer)

    def unsubscribe(self, observer: Observer) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    def publish(self, message: str) -> None:
        # El publicador conoce el contrato update, no los detalles de cada observador.
        # La copia permite recorrer la lista aunque un observador cambie sus suscripciones.
        for observer in self._observers.copy():
            observer.update(message)


def main() -> None:
    publisher = NewsPublisher()
    alex = UserObserver("Alex")
    sam = UserObserver("Sam")
    publisher.subscribe(alex)
    publisher.subscribe(sam)
    publisher.publish("A new Python article is available.")

    # Después de cancelar la suscripción, Alex deja de recibir las siguientes publicaciones.
    publisher.unsubscribe(alex)
    publisher.publish("A new design patterns article is available.")


if __name__ == "__main__":
    main()
