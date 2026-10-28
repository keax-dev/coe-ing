# Tema: bases aisladas para probar el mismo adaptador con SQLite y PostgreSQL.

import os
from collections.abc import Iterator
from pathlib import Path
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.schema import CreateSchema, DropSchema

from src.infrastructure.config.settings import Settings
from src.infrastructure.output.adapter.repository.entity.institution_entity import Base
from src.main import create_app


@pytest.fixture(params=["sqlite", "postgresql"])
def session_factory(
    request: pytest.FixtureRequest, tmp_path: Path
) -> Iterator[sessionmaker[Session]]:
    if request.param == "sqlite":
        engine = create_engine(
            f"sqlite+pysqlite:///{tmp_path / 'test.db'}", connect_args={"check_same_thread": False}
        )
        Base.metadata.create_all(engine)
        try:
            yield sessionmaker(bind=engine, expire_on_commit=False)
        finally:
            engine.dispose()
        return

    if os.getenv("RUN_POSTGRES_TESTS") != "1":
        pytest.skip("Set RUN_POSTGRES_TESTS=1 to use an isolated PostgreSQL schema.")
    engine = create_engine(Settings().sqlalchemy_url, connect_args={"connect_timeout": 5})
    schema = f"test_institution_{uuid4().hex}"
    with engine.begin() as connection:
        connection.execute(CreateSchema(schema))
    isolated_engine = engine.execution_options(schema_translate_map={None: schema})
    try:
        # El esquema generado es exclusivo de esta prueba: public.institution permanece intacta.
        Base.metadata.create_all(isolated_engine)
        yield sessionmaker(bind=isolated_engine, expire_on_commit=False)
    finally:
        with engine.begin() as connection:
            connection.execute(DropSchema(schema, cascade=True))
        engine.dispose()


@pytest.fixture
def client(session_factory: sessionmaker[Session]) -> Iterator[TestClient]:
    with TestClient(create_app(session_factory)) as test_client:
        yield test_client
