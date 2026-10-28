# Tema: contratos del servicio y confirmación explícita por caso de uso.

from unittest.mock import MagicMock, Mock

import pytest

from src.education.clean.application.port.education_repository import EducationRepository
from src.education.clean.application.port.institution_lookup import InstitutionLookup
from src.education.clean.application.port.unit_of_work import UnitOfWork
from src.education.clean.application.service.education_service import EducationService
from src.education.clean.domain.exception.education_errors import (
    ActiveInstitutionNotFound,
    EducationNotFound,
    EducationPersistenceFailure,
    InvalidEducation,
)
from src.education.clean.domain.model.education import Education


def sample(**changes) -> Education:
    return Education(
        **(
            dict(
                education_title="Degree",
                education_place="Quito",
                education_end="Present",
                education_position=0,
                institution_id=1,
            )
            | changes
        )
    )


@pytest.fixture
def work():
    work = MagicMock(spec=UnitOfWork)
    work.__enter__.return_value = work
    work.educations = Mock(spec=EducationRepository)
    work.institutions = Mock(spec=InstitutionLookup)
    return work


def test_creation_requires_active_institution(work) -> None:
    work.institutions.exists_active.return_value = False
    with pytest.raises(ActiveInstitutionNotFound):
        EducationService(lambda: work).create(sample())
    work.institutions.exists_active.assert_called_once_with(1, lock=True)
    work.educations.create.assert_not_called()
    work.commit.assert_not_called()


def test_create_commits_and_returns_domain_entity(work) -> None:
    work.institutions.exists_active.return_value = True
    work.educations.create.return_value = sample(education_id=1, version=0)
    result = EducationService(lambda: work).create(sample())
    assert result.version == 0
    work.educations.create.assert_called_once_with(sample())
    work.commit.assert_called_once()


@pytest.mark.parametrize(
    "changes", [{"education_id": 1}, {"version": 0}, {"education_deleted": True}]
)
def test_invalid_creation_does_not_open_transaction(changes: dict) -> None:
    factory = Mock()
    with pytest.raises(InvalidEducation):
        EducationService(factory).create(sample(**changes))
    factory.assert_not_called()


def test_missing_update_does_not_write_or_commit(work) -> None:
    work.educations.find_by_id.return_value = None
    with pytest.raises(EducationNotFound):
        EducationService(lambda: work).update(sample(education_id=1, version=0))
    work.educations.update.assert_not_called()
    work.commit.assert_not_called()


def test_write_failure_does_not_confirm(work) -> None:
    work.institutions.exists_active.return_value = True
    work.educations.create.side_effect = EducationPersistenceFailure("Unavailable")
    with pytest.raises(EducationPersistenceFailure):
        EducationService(lambda: work).create(sample())
    work.commit.assert_not_called()
    assert work.__exit__.call_args.args[0] is EducationPersistenceFailure


def test_read_does_not_commit(work) -> None:
    work.educations.find_by_id.return_value = sample(education_id=1, version=0)
    assert EducationService(lambda: work).get(1).education_id == 1
    work.commit.assert_not_called()
