# Tema: arranque de FastAPI y conexión de los adaptadores de infraestructura.

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import Engine
from sqlalchemy.orm import Session, sessionmaker

from src.education.clean.presentation.dependency.education_dependencies import (
    configure_education_service,
)
from src.education.clean.presentation.exception.education_exception_handlers import (
    register_education_handlers,
)
from src.education.clean.presentation.router.education_router import router as education_router
from src.institution.hexagonal.infrastructure.config.application_configuration import (
    configure_institution_service,
)
from src.institution.hexagonal.infrastructure.input.adapter.rest.exception_handlers import (
    register_exception_handlers,
)
from src.institution.hexagonal.infrastructure.input.adapter.rest.institution_controller import (
    router,
)
from src.shared.config.database_configuration import configure_database
from src.shared.config.settings import Settings


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

    application = FastAPI(title="Institution and Education API", version="1.1.0", lifespan=lifespan)
    application.state.institution_service = configure_institution_service(session_factory)
    application.state.education_service = configure_education_service(session_factory)
    register_exception_handlers(application)
    register_education_handlers(application)
    application.include_router(router)
    application.include_router(education_router)
    return application


app = create_app()
