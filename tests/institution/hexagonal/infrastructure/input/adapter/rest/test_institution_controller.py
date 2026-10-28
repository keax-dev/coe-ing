# Tema: contrato REST, borrado lógico y control optimista del CRUD completo.


import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session, sessionmaker

from src.institution.hexagonal.infrastructure.output.adapter.repository.entity.institution_entity import (
    InstitutionEntity,
)

BASE = "/api/v1/institutions"
PAYLOAD = {
    "institutionName": "Example University",
    "institutionNameEs": "Universidad de ejemplo",
    "institutionUrl": "https://example.edu",
}


def create(client: TestClient) -> dict:
    response = client.post(BASE, json=PAYLOAD)
    assert response.status_code == 201, response.text
    return response.json()


def test_full_crud_and_soft_delete(
    client: TestClient, session_factory: sessionmaker[Session]
) -> None:
    created = create(client)
    institution_id = created["institutionId"]
    assert created["version"] == 0
    assert created["institutionDeleted"] is False
    assert client.get(f"{BASE}/{institution_id}").json() == created
    assert client.get(BASE).json() == [created]

    update = {
        **PAYLOAD,
        "institutionName": "Updated University",
        "institutionNameEs": None,
        "version": 0,
    }
    response = client.put(f"{BASE}/{institution_id}", json=update)
    assert response.status_code == 200
    assert response.json()["version"] == 1
    assert response.json()["institutionName"] == "Updated University"
    assert response.json()["institutionNameEs"] is None

    assert client.delete(f"{BASE}/{institution_id}?version=1").status_code == 204
    assert client.get(f"{BASE}/{institution_id}").status_code == 404
    assert client.get(BASE).json() == []
    assert client.put(f"{BASE}/{institution_id}", json={**update, "version": 2}).status_code == 404
    assert client.delete(f"{BASE}/{institution_id}?version=2").status_code == 404
    with session_factory() as session:
        entity = session.get(InstitutionEntity, institution_id)
        assert entity is not None
        assert entity.institution_deleted is True
        assert entity.version == 2


def test_stale_update_and_delete_are_rejected(client: TestClient) -> None:
    institution_id = create(client)["institutionId"]
    first_update = client.put(f"{BASE}/{institution_id}", json={**PAYLOAD, "version": 0})
    assert first_update.status_code == 200
    stale = client.put(f"{BASE}/{institution_id}", json={**PAYLOAD, "version": 0})
    assert stale.status_code == 409
    assert stale.json()["code"] == "VERSION_CONFLICT"
    assert client.delete(f"{BASE}/{institution_id}?version=0").status_code == 409
    assert client.get(f"{BASE}/{institution_id}").json()["version"] == 1


@pytest.mark.parametrize(
    "payload",
    [
        {"institutionName": " "},
        {"institutionName": "x" * 256},
        {"institutionName": "Valid", "institutionUrl": "x" * 2049},
        {"institutionName": "Valid", "institutionNameEs": "x" * 256},
        {"institutionName": "Valid", "institutionDeleted": True},
        {"institutionName": "Valid", "version": 0},
        {},
    ],
)
def test_create_validation(client: TestClient, payload: dict) -> None:
    assert client.post(BASE, json=payload).status_code == 422
    assert client.get(BASE).json() == []


def test_missing_resources_versions_and_invalid_pagination(client: TestClient) -> None:
    assert client.get(f"{BASE}/999999").status_code == 404
    assert client.put(f"{BASE}/999999", json={**PAYLOAD, "version": 0}).status_code == 404
    assert client.delete(f"{BASE}/999999?version=0").status_code == 404
    institution_id = create(client)["institutionId"]
    assert client.put(f"{BASE}/{institution_id}", json=PAYLOAD).status_code == 422
    assert (
        client.put(f"{BASE}/{institution_id}", json={**PAYLOAD, "version": True}).status_code == 422
    )
    assert client.delete(f"{BASE}/{institution_id}").status_code == 422
    assert client.get(f"{BASE}?limit=101").status_code == 422
    assert client.get(f"{BASE}?offset=-1").status_code == 422
    assert client.get(f"{BASE}/0").status_code == 422


def test_pagination_and_location(client: TestClient) -> None:
    first = client.post(BASE, json=PAYLOAD)
    second = create(client)
    assert first.headers["Location"] == f"{BASE}/{first.json()['institutionId']}"
    assert client.get(f"{BASE}?offset=1&limit=1").json() == [second]
