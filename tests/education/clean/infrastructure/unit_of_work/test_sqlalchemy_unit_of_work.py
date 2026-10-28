# Tema: commit, rollback, cierre de sesión y traducción de fallos técnicos.

from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm import Session, sessionmaker

from src.education.clean.domain.exception.education_errors import (
    EducationPersistenceConflict,
    EducationPersistenceFailure,
)
from src.education.clean.domain.model.education import Education
from src.education.clean.infrastructure.unit_of_work.sqlalchemy_unit_of_work import (
    SQLAlchemyUnitOfWork,
)


def sample(institution_id: int) -> Education:
    return Education(
        education_title="Degree",
        education_place="Quito",
        education_end="Present",
        education_position=0,
        institution_id=institution_id,
    )


def test_unconfirmed_work_is_rolled_back(
    client: TestClient, session_factory: sessionmaker[Session]
) -> None:
    parent = client.post("/api/v1/institutions", json={"institutionName": "University"}).json()
    with SQLAlchemyUnitOfWork(session_factory) as work:
        work.educations.create(sample(parent["institutionId"]))
    with SQLAlchemyUnitOfWork(session_factory) as work:
        assert work.educations.find_all(0, 100, None, None) == []


def test_commit_persists_and_failure_rolls_back(
    client: TestClient, session_factory: sessionmaker[Session]
) -> None:
    parent = client.post("/api/v1/institutions", json={"institutionName": "University"}).json()
    with SQLAlchemyUnitOfWork(session_factory) as work:
        created = work.educations.create(sample(parent["institutionId"]))
        work.commit()
    with pytest.raises(ValueError, match="Simulated"):
        with SQLAlchemyUnitOfWork(session_factory) as work:
            work.educations.create(sample(parent["institutionId"]))
            raise ValueError("Simulated failure")
    with SQLAlchemyUnitOfWork(session_factory) as work:
        assert work.educations.find_all(0, 100, None, None) == [created]


@pytest.mark.parametrize(
    "error, expected",
    [
        (OperationalError("SQL", {}, Exception("secret")), EducationPersistenceFailure),
        (IntegrityError("SQL", {}, Exception("secret")), EducationPersistenceConflict),
    ],
)
def test_commit_failure_closes_session(error, expected) -> None:
    session = Mock(spec=Session)
    session.commit.side_effect = error
    with pytest.raises(expected):
        with SQLAlchemyUnitOfWork(Mock(return_value=session)) as work:
            work.commit()
    session.rollback.assert_called_once()
    session.close.assert_called_once()


def test_begin_failure_closes_session() -> None:
    session = Mock(spec=Session)
    session.begin.side_effect = OperationalError("SQL", {}, Exception("secret"))
    with pytest.raises(EducationPersistenceFailure):
        with SQLAlchemyUnitOfWork(Mock(return_value=session)):
            pass
    session.close.assert_called_once()
