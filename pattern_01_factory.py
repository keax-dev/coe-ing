# Tema: patrón Factory mediante una fábrica simple de notificaciones.

from abc import ABC, abstractmethod


class Notification(ABC):
    @abstractmethod
    def send(self, message: str) -> str:
        raise NotImplementedError


class EmailNotification(Notification):
    def send(self, message: str) -> str:
        return f"Email: {message}"


class SMSNotification(Notification):
    def send(self, message: str) -> str:
        return f"SMS: {message}"


def create_notification(channel: str) -> Notification:
    # La fábrica concentra la elección de la clase y la creación del objeto.
    notification_types = {"email": EmailNotification, "sms": SMSNotification}
    notification_type = notification_types.get(channel)
    if notification_type is None:
        raise ValueError(f"Unsupported notification channel: {channel}")
    return notification_type()


def main() -> None:
    for channel in ["email", "sms"]:
        # El consumidor usa el mismo contrato sin tener que construir cada clase concreta.
        notification = create_notification(channel)
        print(notification.send("Your order is ready."))


if __name__ == "__main__":
    main()
