# Tema: arranque de FastAPI y conexión de los adaptadores de infraestructura.

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import Engine
from sqlalchemy.orm import Session, sessionmaker

from institution.infrastructure.config.application_configuration import (
    configure_institution_service,
)
from institution.infrastructure.config.database_configuration import configure_database
from institution.infrastructure.config.settings import Settings
from institution.infrastructure.input.adapter.rest.exception_handlers import (
    register_exception_handlers,
)
from institution.infrastructure.input.adapter.rest.institution_controller import router


def create_app(session_factory: sessionmaker[Session] | None = None) -> FastAPI:
    engine: Engine | None = None
    if session_factory is None:
        engine, session_factory = configure_database(Settings())

    @asynccontextmanager
    async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
        try:
            yield
        finally:
            if engine is not None:
                engine.dispose()

    application = FastAPI(title="Institution API", version="1.0.0", lifespan=lifespan)
    application.state.institution_service = configure_institution_service(session_factory)
    register_exception_handlers(application)
    application.include_router(router)
    return application


app = create_app()
