# Tema: mapeo SQLAlchemy de la tabla institution existente.

from sqlalchemy import BigInteger, Boolean, Identity, Integer, String, false
from sqlalchemy.orm import Mapped, mapped_column

from src.shared.persistence.base import Base


class InstitutionEntity(Base):
    __tablename__ = "institution"

    # PostgreSQL conserva BIGINT; la variante permite probar el adaptador con SQLite aislado.
    institution_id: Mapped[int] = mapped_column(
        BigInteger().with_variant(Integer, "sqlite"), Identity(), primary_key=True
    )
    institution_name: Mapped[str] = mapped_column(String(255), nullable=False)
    institution_name_es: Mapped[str | None] = mapped_column(String(255))
    institution_url: Mapped[str | None] = mapped_column(String(2048))
    institution_deleted: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default=false()
    )
    version: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)
