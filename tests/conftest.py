# Tema: bases SQLite temporales para probar ambos CRUD sin tocar los datos locales.

from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session, sessionmaker

from src.main import create_app
from src.shared.config.database_configuration import configure_database
from src.shared.config.settings import Settings
from src.shared.persistence.base import Base


@pytest.fixture
def session_factory(tmp_path: Path) -> Iterator[sessionmaker[Session]]:
    engine, factory = configure_database(
        Settings(_env_file=None, DB_URL=f"sqlite:///{tmp_path / 'test.db'}")
    )
    try:
        Base.metadata.create_all(engine)
        yield factory
    finally:
        engine.dispose()


@pytest.fixture
def client(session_factory: sessionmaker[Session]) -> Iterator[TestClient]:
    with TestClient(create_app(session_factory)) as test_client:
        yield test_client
