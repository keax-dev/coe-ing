# Tema: CRUD de educación, relación institucional, filtros y borrado lógico.

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session, sessionmaker

from src.education.clean.infrastructure.model.education_model import EducationModel

BASE = "/api/v1/educations"
FIELDS = dict(
    educationTitle="Software Engineering",
    educationTitleEs="Ingeniería de software",
    educationPlace="Quito",
    educationStart="September 2020",
    educationStartEs="Septiembre 2020",
    educationEnd="Present",
    educationEndEs="Actualidad",
    educationPosition=1,
)


@pytest.fixture
def payload(client: TestClient) -> dict:
    parent = client.post("/api/v1/institutions", json={"institutionName": "University"})
    assert parent.status_code == 201
    return FIELDS | {"institutionId": parent.json()["institutionId"]}


def create(client: TestClient, payload: dict) -> dict:
    response = client.post(BASE, json=payload)
    assert response.status_code == 201, response.text
    assert response.headers["Location"] == f"{BASE}/{response.json()['educationId']}"
    return response.json()


def test_full_crud(
    client: TestClient, payload: dict, session_factory: sessionmaker[Session]
) -> None:
    created = create(client, payload)
    education_id = created["educationId"]
    assert created["educationVisible"] is True
    assert created["educationDeleted"] is False
    assert created["version"] == 0
    assert client.get(f"{BASE}/{education_id}").json() == created
    assert client.get(BASE).json() == [created]
    update = payload | {
        "educationTitle": "Updated degree",
        "educationVisible": False,
        "educationStartEs": None,
        "version": 0,
    }
    response = client.put(f"{BASE}/{education_id}", json=update)
    assert response.status_code == 200, response.text
    assert response.json()["version"] == 1
    assert response.json()["educationVisible"] is False
    assert response.json()["educationStartEs"] is None
    assert len(client.get(BASE).json()) == 1
    assert client.get(f"{BASE}?visible=true").json() == []
    assert (
        len(client.get(f"{BASE}?visible=false&institutionId={payload['institutionId']}").json())
        == 1
    )
    assert client.delete(f"{BASE}/{education_id}?version=1").status_code == 204
    assert client.get(f"{BASE}/{education_id}").status_code == 404
    assert client.get(BASE).json() == []
    assert client.put(f"{BASE}/{education_id}", json=update | {"version": 2}).status_code == 404
    assert client.delete(f"{BASE}/{education_id}?version=2").status_code == 404
    with session_factory() as session:
        record = session.get(EducationModel, education_id)
        assert record is not None and record.education_deleted
        assert record.version == 2
        assert record.institution_id == payload["institutionId"]


def test_stale_versions_cannot_write(client: TestClient, payload: dict) -> None:
    education_id = create(client, payload)["educationId"]
    assert client.put(f"{BASE}/{education_id}", json=payload | {"version": 0}).status_code == 200
    stale = client.put(f"{BASE}/{education_id}", json=payload | {"version": 0})
    assert stale.status_code == 409
    assert stale.json()["code"] == "EDUCATION_VERSION_CONFLICT"
    assert client.delete(f"{BASE}/{education_id}?version=0").status_code == 409


def test_relation_requires_active_institution(client: TestClient, payload: dict) -> None:
    assert client.post(BASE, json=payload | {"institutionId": 999999}).status_code == 404
    created = create(client, payload)
    parent_id = payload["institutionId"]
    assert client.delete(f"/api/v1/institutions/{parent_id}?version=0").status_code == 204
    assert client.post(BASE, json=payload).status_code == 404
    # El borrado del padre no es una cascada; conserva la relación histórica ya registrada.
    assert client.get(f"{BASE}/{created['educationId']}").status_code == 200
    assert (
        client.put(f"{BASE}/{created['educationId']}", json=payload | {"version": 0}).status_code
        == 404
    )
    other = client.post("/api/v1/institutions", json={"institutionName": "Other"}).json()
    response = client.put(
        f"{BASE}/{created['educationId']}",
        json=payload | {"institutionId": other["institutionId"], "version": 0},
    )
    assert response.status_code == 200
    assert response.json()["institutionId"] == other["institutionId"]


@pytest.mark.parametrize(
    "changes",
    [
        {"educationTitle": " "},
        {"educationPlace": ""},
        {"educationEnd": None},
        {"educationTitle": "x" * 256},
        {"educationPosition": True},
        {"educationPosition": 2**31},
        {"educationVisible": "true"},
        {"institutionId": 0},
        {"educationDeleted": True},
        {"version": 0},
        {"educationId": 1},
    ],
)
def test_invalid_requests_do_not_persist(client: TestClient, payload: dict, changes: dict) -> None:
    assert client.post(BASE, json=payload | changes).status_code == 422
    assert client.get(BASE).json() == []


def test_order_filters_pagination_and_missing_versions(client: TestClient, payload: dict) -> None:
    first = create(client, payload | {"educationPosition": 5})
    second = create(client, payload | {"educationPosition": -1})
    assert client.get(BASE).json() == [second, first]
    assert client.get(f"{BASE}?offset=1&limit=1").json() == [first]
    assert client.get(f"{BASE}?institutionId=999999").json() == []
    assert client.get(f"{BASE}?limit=101").status_code == 422
    assert client.put(f"{BASE}/{first['educationId']}", json=payload).status_code == 422
    assert client.delete(f"{BASE}/{first['educationId']}").status_code == 422
    assert client.get(f"{BASE}/999999").status_code == 404
    assert client.put(f"{BASE}/999999", json=payload | {"version": 0}).status_code == 404
    assert client.delete(f"{BASE}/999999?version=0").status_code == 404
