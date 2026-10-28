# Tema: consultas, control optimista y ausencia de commits internos en el repositorio.

from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from threading import Barrier

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session, sessionmaker

from src.education.clean.domain.exception.education_errors import EducationVersionConflict
from src.education.clean.domain.model.education import Education
from src.education.clean.infrastructure.repository.education_repository import (
    SQLAlchemyEducationRepository,
)
from src.education.clean.presentation.dependency.education_dependencies import (
    configure_education_service,
)


def sample(institution_id: int) -> Education:
    return Education(
        education_title="Degree",
        education_place="Quito",
        education_end="Present",
        education_position=0,
        institution_id=institution_id,
    )


def test_repository_flush_does_not_commit(
    client: TestClient, session_factory: sessionmaker[Session]
) -> None:
    parent = client.post("/api/v1/institutions", json={"institutionName": "University"}).json()
    with session_factory() as session:
        created = SQLAlchemyEducationRepository(session).create(sample(parent["institutionId"]))
        assert created.education_id is not None
        session.rollback()
    with session_factory() as session:
        assert SQLAlchemyEducationRepository(session).find_by_id(created.education_id) is None


def test_concurrent_updates_allow_only_one_version(
    client: TestClient, session_factory: sessionmaker[Session]
) -> None:
    parent = client.post("/api/v1/institutions", json={"institutionName": "University"}).json()
    service = configure_education_service(session_factory)
    created = service.create(sample(parent["institutionId"]))
    barrier = Barrier(2)

    def update(title: str) -> str:
        barrier.wait(timeout=10)
        try:
            service.update(replace(created, education_title=title))
            return "updated"
        except EducationVersionConflict:
            return "conflict"

    with ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(update, ["First", "Second"]))
    assert sorted(results) == ["conflict", "updated"]
    assert service.get(created.education_id).version == 1
