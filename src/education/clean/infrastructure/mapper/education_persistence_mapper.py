# Tema: conversión de registros ORM a entidades de negocio sin filtrar SQLAlchemy hacia dentro.

from dataclasses import asdict, fields

from src.education.clean.domain.model.education import Education
from src.education.clean.infrastructure.model.education_model import EducationModel


class EducationPersistenceMapper:
    @staticmethod
    def to_record(education: Education) -> EducationModel:
        values = asdict(education)
        # La identidad y el estado inicial pertenecen al almacenamiento, no al cliente.
        values.pop("education_id")
        values.update(education_deleted=False, version=0)
        return EducationModel(**values)

    @staticmethod
    def to_entity(record: EducationModel) -> Education:
        return Education(**{field.name: getattr(record, field.name) for field in fields(Education)})
