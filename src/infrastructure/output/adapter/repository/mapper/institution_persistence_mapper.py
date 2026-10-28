# Tema: conversiones explícitas entre entidades SQL y modelos de dominio.

from src.domain.model.institution import Institution
from src.infrastructure.output.adapter.repository.entity.institution_entity import (
    InstitutionEntity,
)


class InstitutionPersistenceMapper:
    @staticmethod
    def to_entity(institution: Institution) -> InstitutionEntity:
        return InstitutionEntity(
            institution_name=institution.institution_name,
            institution_name_es=institution.institution_name_es,
            institution_url=institution.institution_url,
            institution_deleted=False,
            version=0,
        )

    @staticmethod
    def to_domain(entity: InstitutionEntity) -> Institution:
        return Institution(
            institution_id=entity.institution_id,
            institution_name=entity.institution_name,
            institution_name_es=entity.institution_name_es,
            institution_url=entity.institution_url,
            institution_deleted=entity.institution_deleted,
            version=entity.version,
        )
