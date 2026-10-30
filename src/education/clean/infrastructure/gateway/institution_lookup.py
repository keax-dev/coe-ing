# Tema: consulta de instituciones dentro de la transacción de la unidad de trabajo.

from sqlalchemy import BigInteger, Boolean, Column, MetaData, Table, select
from sqlalchemy.orm import Session

from src.education.clean.application.port.institution_lookup import InstitutionLookup

# Este gateway no importa la implementación hexagonal de instituciones.
institution_table = Table(
    "institution",
    MetaData(),
    Column("institution_id", BigInteger),
    Column("institution_deleted", Boolean),
)


class SQLAlchemyInstitutionLookup(InstitutionLookup):
    def __init__(self, session: Session) -> None:
        self._session = session

    def exists_active(self, institution_id: int) -> bool:
        query = select(institution_table.c.institution_id).where(
            institution_table.c.institution_id == institution_id,
            institution_table.c.institution_deleted.is_(False),
        )
        return self._session.scalar(query) is not None
