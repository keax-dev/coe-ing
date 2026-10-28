# Tema: concurrencia y control optimista en el adaptador de persistencia.

from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from threading import Barrier

from sqlalchemy.orm import Session, sessionmaker

from src.institution.domain.exception.institution_errors import InstitutionVersionConflict
from src.institution.domain.model.institution import Institution
from src.institution.infrastructure.config.application_configuration import (
    configure_institution_service,
)


def test_concurrent_writes_allow_only_one_version(session_factory: sessionmaker[Session]) -> None:
    service = configure_institution_service(session_factory)
    created = service.create(Institution(institution_name="Concurrent University"))
    barrier = Barrier(2)

    def update(name: str) -> str:
        barrier.wait(timeout=10)
        try:
            service.update(replace(created, institution_name=name))
            return "updated"
        except InstitutionVersionConflict:
            return "conflict"

    with ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(update, ["First", "Second"]))
    assert sorted(results) == ["conflict", "updated"]
    assert service.get(created.institution_id).version == 1
