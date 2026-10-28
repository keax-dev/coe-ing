# Tema: modelo de dominio independiente de HTTP y de persistencia.

from dataclasses import dataclass

from src.domain.exception.institution_errors import InvalidInstitution


@dataclass(frozen=True, slots=True)
class Institution:
    institution_name: str
    institution_name_es: str | None = None
    institution_url: str | None = None
    institution_id: int | None = None
    institution_deleted: bool = False
    version: int | None = None

    def __post_init__(self) -> None:
        if not self.institution_name.strip() or len(self.institution_name) > 255:
            raise InvalidInstitution("Institution name must contain between 1 and 255 characters.")
        if self.institution_name_es is not None and len(self.institution_name_es) > 255:
            raise InvalidInstitution("Spanish institution name cannot exceed 255 characters.")
        if self.institution_url is not None and len(self.institution_url) > 2048:
            raise InvalidInstitution("Institution URL cannot exceed 2048 characters.")
        if self.institution_id is not None and self.institution_id <= 0:
            raise InvalidInstitution("Institution ID must be positive.")
        if self.version is not None and self.version < 0:
            raise InvalidInstitution("Version cannot be negative.")
