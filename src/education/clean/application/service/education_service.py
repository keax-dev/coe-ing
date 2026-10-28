# Tema: casos de uso que coordinan validación y persistencia en una sola unidad de trabajo.

from src.education.clean.application.port.unit_of_work import UnitOfWork, UnitOfWorkFactory
from src.education.clean.domain.exception.education_errors import (
    ActiveInstitutionNotFound,
    EducationNotFound,
    InvalidEducation,
)
from src.education.clean.domain.model.education import Education


class EducationService:
    def __init__(self, unit_of_work_factory: UnitOfWorkFactory) -> None:
        self._unit_of_work_factory = unit_of_work_factory

    @staticmethod
    def _require_institution(work: UnitOfWork, institution_id: int) -> None:
        # La búsqueda y la escritura comparten sesión; el bloqueo dura hasta el commit.
        if not work.institutions.exists_active(institution_id, lock=True):
            raise ActiveInstitutionNotFound("Institution was not found or is deleted.")

    def create(self, education: Education) -> Education:
        if (
            education.education_id is not None
            or education.version is not None
            or education.education_deleted
        ):
            raise InvalidEducation(
                "New education cannot specify identity, version or deletion state."
            )
        with self._unit_of_work_factory() as work:
            self._require_institution(work, education.institution_id)
            result = work.educations.create(education)
            work.commit()
            return result

    def get(self, education_id: int) -> Education:
        with self._unit_of_work_factory() as work:
            education = work.educations.find_by_id(education_id)
            if education is None:
                raise EducationNotFound("Education was not found.")
            return education

    def list(
        self,
        offset: int,
        limit: int,
        institution_id: int | None = None,
        visible: bool | None = None,
    ) -> list[Education]:
        if offset < 0 or not 1 <= limit <= 100:
            raise InvalidEducation("Pagination requires offset >= 0 and limit between 1 and 100.")
        if institution_id is not None and institution_id <= 0:
            raise InvalidEducation("Institution ID must be positive.")
        with self._unit_of_work_factory() as work:
            return work.educations.find_all(offset, limit, institution_id, visible)

    def update(self, education: Education) -> Education:
        if (
            education.education_id is None
            or education.version is None
            or education.education_deleted
        ):
            raise InvalidEducation("Updates require identity and version; use delete for deletion.")
        with self._unit_of_work_factory() as work:
            if work.educations.find_by_id(education.education_id) is None:
                raise EducationNotFound("Education was not found.")
            self._require_institution(work, education.institution_id)
            result = work.educations.update(education)
            work.commit()
            return result

    def delete(self, education_id: int, version: int) -> None:
        if education_id <= 0 or version < 0:
            raise InvalidEducation("Deletion requires a positive ID and nonnegative version.")
        with self._unit_of_work_factory() as work:
            work.educations.soft_delete(education_id, version)
            work.commit()
