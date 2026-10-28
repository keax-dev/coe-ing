# Tema: contrato de transacción independiente de SQLAlchemy.

from collections.abc import Callable
from types import TracebackType
from typing import Protocol

from src.education.clean.application.port.education_repository import EducationRepository
from src.education.clean.application.port.institution_lookup import InstitutionLookup


class UnitOfWork(Protocol):
    educations: EducationRepository
    institutions: InstitutionLookup

    def __enter__(self) -> "UnitOfWork": ...

    def __exit__(
        self,
        exception_type: type[BaseException] | None,
        exception: BaseException | None,
        traceback: TracebackType | None,
    ) -> None: ...

    def commit(self) -> None: ...

    def rollback(self) -> None: ...


UnitOfWorkFactory = Callable[[], UnitOfWork]
