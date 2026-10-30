# Tema: persistencia SQLite entre conexiones, transacciones y migraciones de un archivo local.

import os
import subprocess
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import inspect, select, text
from sqlalchemy.exc import IntegrityError

from src.education.clean.infrastructure.model.education_model import EducationModel
from src.institution.hexagonal.infrastructure.output.adapter.repository.entity.institution_entity import (
    InstitutionEntity,
)
from src.main import create_app
from src.shared.config.database_configuration import configure_database
from src.shared.config.settings import Settings
from src.shared.persistence.base import Base


def settings_for(path: Path) -> Settings:
    return Settings(_env_file=None, DB_URL=f"sqlite:///{path}")


def test_folder_foreign_keys_and_rollback(tmp_path: Path) -> None:
    engine, factory = configure_database(settings_for(tmp_path / "nested" / "portfolio.db"))
    try:
        assert (tmp_path / "nested").is_dir()
        Base.metadata.create_all(engine)
        with engine.connect() as connection:
            assert connection.scalar(text("PRAGMA foreign_keys")) == 1
        with factory() as session:
            session.add(
                InstitutionEntity(
                    institution_name="Uncommitted", version=0, institution_deleted=False
                )
            )
            session.flush()
            session.rollback()
        with factory() as session:
            assert session.scalar(select(InstitutionEntity)) is None
        with pytest.raises(IntegrityError):
            with factory.begin() as session:
                session.add(
                    EducationModel(
                        education_title="Degree",
                        education_place="Quito",
                        education_end="Present",
                        education_position=0,
                        institution_id=999999,
                    )
                )
    finally:
        engine.dispose()


def test_both_resources_survive_app_and_engine_restart(tmp_path: Path) -> None:
    settings = settings_for(tmp_path / "portfolio.db")
    engine, factory = configure_database(settings)
    try:
        Base.metadata.create_all(engine)
        with TestClient(create_app(factory)) as client:
            parent = client.post(
                "/api/v1/institutions", json={"institutionName": "Persisted University"}
            )
            assert parent.status_code == 201
            institution = parent.json()
            response = client.post(
                "/api/v1/educations",
                json={
                    "educationTitle": "Persisted degree",
                    "educationPlace": "Quito",
                    "educationEnd": "Present",
                    "educationPosition": 0,
                    "institutionId": institution["institutionId"],
                },
            )
            assert response.status_code == 201
            education = response.json()
    finally:
        engine.dispose()
    engine, factory = configure_database(settings)
    try:
        with TestClient(create_app(factory)) as client:
            assert (
                client.get(f"/api/v1/institutions/{institution['institutionId']}").json()
                == institution
            )
            assert client.get(f"/api/v1/educations/{education['educationId']}").json() == education
    finally:
        engine.dispose()


def test_alembic_cli_creates_persistent_sqlite_schema(tmp_path: Path) -> None:
    path = tmp_path / "new" / "portfolio.db"
    environment = {**os.environ, "DB_URL": f"sqlite:///{path}", "PYTHONDONTWRITEBYTECODE": "1"}
    result = subprocess.run(
        [sys.executable, "-B", "-m", "alembic", "upgrade", "head"],
        cwd=Path(__file__).resolve().parents[3],
        env=environment,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    engine, _factory = configure_database(settings_for(path))
    try:
        with engine.connect() as connection:
            assert {"institution", "education", "alembic_version"} <= set(
                inspect(connection).get_table_names()
            )
            assert connection.scalar(text("SELECT version_num FROM alembic_version")) == "0001"
    finally:
        engine.dispose()
