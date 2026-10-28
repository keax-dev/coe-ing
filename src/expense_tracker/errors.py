# Las excepciones del dominio permiten distinguir datos inválidos de fallos de almacenamiento.


class ExpenseTrackerError(Exception):
    pass


class ExpenseValidationError(ExpenseTrackerError, ValueError):
    pass


class StorageError(ExpenseTrackerError):
    pass
