# Tema: confirmación explícita, rollback y cierre de una sesión compartida por operación.

from types import TracebackType

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker

from src.education.clean.application.port.unit_of_work import UnitOfWork
from src.education.clean.domain.exception.education_errors import (
    EducationPersistenceConflict,
    EducationPersistenceFailure,
)
from src.education.clean.infrastructure.gateway.institution_lookup import (
    SQLAlchemyInstitutionLookup,
)
from src.education.clean.infrastructure.repository.education_repository import (
    SQLAlchemyEducationRepository,
)


def translate_error(error: SQLAlchemyError) -> None:
    if isinstance(error, IntegrityError):
        raise EducationPersistenceConflict("Education violates a database constraint.") from error
    raise EducationPersistenceFailure("Education persistence is unavailable.") from error


class SQLAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self._session_factory = session_factory
        self._session: Session | None = None

    def __enter__(self) -> "SQLAlchemyUnitOfWork":
        try:
            self._session = self._session_factory()
            self._session.begin()
        except SQLAlchemyError as error:
            if self._session is not None:
                self._session.close()
            translate_error(error)
        self.educations = SQLAlchemyEducationRepository(self._session)
        self.institutions = SQLAlchemyInstitutionLookup(self._session)
        return self

    def commit(self) -> None:
        assert self._session is not None
        try:
            self._session.commit()
        except SQLAlchemyError as error:
            translate_error(error)

    def rollback(self) -> None:
        assert self._session is not None
        self._session.rollback()

    def __exit__(
        self,
        exception_type: type[BaseException] | None,
        exception: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        assert self._session is not None
        try:
            # Sin commit explícito, cualquier escritura queda descartada; las lecturas también se cierran.
            self.rollback()
        except SQLAlchemyError as error:
            if exception is None:
                translate_error(error)
        finally:
            self._session.close()
        if isinstance(exception, SQLAlchemyError):
            translate_error(exception)
