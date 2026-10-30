# Tema: conexión SQLite persistente con claves foráneas y transacciones explícitas.

from pathlib import Path

from sqlalchemy import Engine, create_engine, event
from sqlalchemy.orm import Session, sessionmaker

from src.shared.config.settings import Settings


def configure_database(settings: Settings) -> tuple[Engine, sessionmaker[Session]]:
    url = settings.sqlalchemy_url
    # SQLite crea el archivo, pero no la carpeta que lo contiene.
    path = Path(url.database).expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    engine = create_engine(
        url.set(database=str(path)),
        pool_pre_ping=True,
        connect_args={"check_same_thread": False, "timeout": 30},
    )

    @event.listens_for(engine, "connect")
    def configure_sqlite(connection, _record):
        # SQLAlchemy controla BEGIN; activamos las claves foráneas en cada conexión.
        connection.isolation_level = None
        cursor = connection.cursor()
        try:
            cursor.execute("PRAGMA foreign_keys=ON")
        finally:
            cursor.close()

    @event.listens_for(engine, "begin")
    def begin_sqlite(connection):
        # Reservamos la escritura antes de validar para evitar carreras entre lecturas y cambios.
        connection.exec_driver_sql("BEGIN IMMEDIATE")

    # No ejecutamos create_all: la tabla real debe conservar su esquema y datos.
    return engine, sessionmaker(bind=engine, expire_on_commit=False)
