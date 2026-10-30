# Tema: migraciones manuales con configuración compartida y metadatos de ambas funcionalidades.

from alembic import context
from sqlalchemy import Connection

from src.education.clean.infrastructure.model.education_model import EducationModel
from src.institution.hexagonal.infrastructure.output.adapter.repository.entity.institution_entity import (
    InstitutionEntity,
)
from src.shared.config.database_configuration import configure_database
from src.shared.config.settings import Settings

config = context.config
# Referenciar ambos modelos registra las dos tablas, incluida su relación de clave foránea.
assert EducationModel.metadata is InstitutionEntity.metadata
target_metadata = EducationModel.metadata


def include_object(object_, name, type_, reflected, compare_to):
    # Autogenerate no debe proponer cambios para tablas ajenas a estas funcionalidades.
    if type_ == "table":
        return name in {table.name for table in target_metadata.tables.values()}
    # La base existente puede tener índices y restricciones administrados fuera de estos modelos.
    if (
        reflected
        and compare_to is None
        and type_ in {"index", "unique_constraint", "foreign_key_constraint", "check_constraint"}
    ):
        return False
    return True


def run_with_connection(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        include_object=include_object,
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_online() -> None:
    connection = config.attributes.get("connection")
    if connection is not None:
        # Las pruebas inyectan una conexión aislada, sin consultar la base de trabajo.
        run_with_connection(connection)
        return
    engine, _session_factory = configure_database(Settings())
    try:
        with engine.connect() as connection:
            run_with_connection(connection)
    finally:
        engine.dispose()


if context.is_offline_mode():
    context.configure(
        url=Settings().sqlalchemy_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()
else:
    run_online()
