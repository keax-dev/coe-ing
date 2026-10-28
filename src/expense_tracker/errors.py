# Tema: jerarquía de excepciones del dominio.


class ExpenseTrackerError(Exception):
    # La interfaz puede capturar toda esta familia sin ocultar errores ajenos al dominio.
    pass


class ExpenseValidationError(ExpenseTrackerError, ValueError):
    # También es ValueError para integrarse con validaciones de valores convencionales.
    pass


class StorageError(ExpenseTrackerError):
    pass
