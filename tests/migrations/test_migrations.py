# Tema: migraciones y adopción de tablas existentes en bases completamente aisladas.

import os
from collections.abc import Iterator
from pathlib import Path
from uuid import uuid4

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import Connection, Index, create_engine, inspect, select, text
from sqlalchemy.schema import CreateSchema, DropSchema

from src.institution.hexagonal.infrastructure.output.adapter.repository.entity.institution_entity import (
    InstitutionEntity,
)
from src.shared.config.settings import Settings
from src.shared.persistence.base import Base

ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(params=["sqlite", "postgresql"])
def migration_connection(
    request: pytest.FixtureRequest, tmp_path: Path
) -> Iterator[tuple[Connection, Config]]:
    schema = None
    if request.param == "postgresql":
        if os.getenv("RUN_POSTGRES_TESTS") != "1":
            pytest.skip(
                "Set RUN_POSTGRES_TESTS=1 to test migrations in an isolated PostgreSQL schema."
            )
        engine = create_engine(Settings().sqlalchemy_url)
        schema = f"test_migration_{uuid4().hex}"
        with engine.begin() as connection:
            connection.execute(CreateSchema(schema))
    else:
        engine = create_engine(f"sqlite:///{tmp_path / 'migration.db'}")
    try:
        with engine.begin() as connection:
            if schema is not None:
                quoted = engine.dialect.identifier_preparer.quote(schema)
                connection.execute(text(f"SET LOCAL search_path TO {quoted}"))
            config = Config(str(ROOT / "alembic.ini"))
            config.attributes["connection"] = connection
            config.attributes["version_table_schema"] = schema
            yield connection, config
    finally:
        if schema is not None:
            with engine.begin() as connection:
                connection.execute(DropSchema(schema, cascade=True))
        engine.dispose()


def test_upgrade_matches_models_and_can_downgrade(migration_connection) -> None:
    connection, config = migration_connection
    command.upgrade(config, "head")
    assert {"institution", "education", "alembic_version"} <= set(
        inspect(connection).get_table_names()
    )
    command.check(config)
    command.downgrade(config, "base")
    assert "institution" not in inspect(connection).get_table_names()
    assert "education" not in inspect(connection).get_table_names()


def test_baseline_stamp_preserves_existing_records(migration_connection) -> None:
    connection, config = migration_connection
    Base.metadata.create_all(connection)
    # Un índice existente ajeno al modelo no debe convertirse en una propuesta de eliminación.
    external_index = Index(
        "external_institution_name_idx", InstitutionEntity.__table__.c.institution_name
    )
    external_index.create(connection)
    InstitutionEntity.__table__.indexes.remove(external_index)
    connection.execute(
        InstitutionEntity.__table__.insert().values(institution_name="Existing University")
    )
    command.stamp(config, "0001")
    command.check(config)
    assert connection.scalar(select(InstitutionEntity.institution_name)) == "Existing University"
    assert "external_institution_name_idx" in {
        index["name"] for index in inspect(connection).get_indexes("institution")
    }
