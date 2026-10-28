# Tema: búsqueda y bloqueo institucional dentro de la sesión del caso de uso.

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session, sessionmaker

from src.education.clean.infrastructure.gateway.institution_lookup import (
    SQLAlchemyInstitutionLookup,
)
from src.institution.hexagonal.infrastructure.output.adapter.repository.entity.institution_entity import (
    InstitutionEntity,
)


def test_active_missing_and_deleted_institutions(
    client: TestClient, session_factory: sessionmaker[Session]
) -> None:
    parent = client.post("/api/v1/institutions", json={"institutionName": "University"}).json()
    with session_factory.begin() as session:
        lookup = SQLAlchemyInstitutionLookup(session)
        assert lookup.exists_active(parent["institutionId"], lock=True)
        assert not lookup.exists_active(999999)
    client.delete(f"/api/v1/institutions/{parent['institutionId']}?version=0")
    with session_factory.begin() as session:
        assert not SQLAlchemyInstitutionLookup(session).exists_active(
            parent["institutionId"], lock=True
        )


def test_lookup_sees_uncommitted_changes_in_same_session(
    session_factory: sessionmaker[Session],
) -> None:
    with session_factory() as session:
        parent = InstitutionEntity(
            institution_name="Uncommitted", institution_deleted=False, version=0
        )
        session.add(parent)
        session.flush()
        assert SQLAlchemyInstitutionLookup(session).exists_active(parent.institution_id)
        parent_id = parent.institution_id
        session.rollback()
    with session_factory() as session:
        assert not SQLAlchemyInstitutionLookup(session).exists_active(parent_id)
