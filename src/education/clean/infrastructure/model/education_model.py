# Tema: detalle SQLAlchemy de la tabla education y su clave foránea.

from sqlalchemy import BigInteger, Boolean, ForeignKey, Identity, Integer, String, false, true
from sqlalchemy.orm import Mapped, mapped_column

from src.shared.persistence.base import Base


class EducationModel(Base):
    __tablename__ = "education"

    education_id: Mapped[int] = mapped_column(
        BigInteger().with_variant(Integer, "sqlite"), Identity(), primary_key=True
    )
    education_title: Mapped[str] = mapped_column(String(255), nullable=False)
    education_title_es: Mapped[str | None] = mapped_column(String(255))
    education_place: Mapped[str] = mapped_column(String(255), nullable=False)
    education_start: Mapped[str | None] = mapped_column(String(255))
    education_start_es: Mapped[str | None] = mapped_column(String(255))
    education_end: Mapped[str] = mapped_column(String(255), nullable=False)
    education_end_es: Mapped[str | None] = mapped_column(String(255))
    education_position: Mapped[int] = mapped_column(Integer, nullable=False)
    education_deleted: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default=false()
    )
    education_visible: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default=true()
    )
    institution_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("institution.institution_id"), nullable=False
    )
    version: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)
