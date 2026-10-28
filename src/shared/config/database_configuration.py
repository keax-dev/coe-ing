# Tema: creación del motor y de sesiones sin modificar el esquema existente.

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.shared.config.settings import Settings


def configure_database(settings: Settings) -> tuple[Engine, sessionmaker[Session]]:
    engine = create_engine(
        settings.sqlalchemy_url, pool_pre_ping=True, connect_args={"connect_timeout": 5}
    )
    # No ejecutamos create_all: la tabla real debe conservar su esquema y datos.
    return engine, sessionmaker(bind=engine, expire_on_commit=False)
