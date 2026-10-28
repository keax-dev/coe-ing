# Tema: entidad de educación con reglas independientes de HTTP y bases de datos.

from dataclasses import dataclass

from src.education.clean.domain.exception.education_errors import InvalidEducation


@dataclass(frozen=True, slots=True)
class Education:
    education_title: str
    education_place: str
    education_end: str
    education_position: int
    institution_id: int
    education_title_es: str | None = None
    education_start: str | None = None
    education_start_es: str | None = None
    education_end_es: str | None = None
    education_visible: bool = True
    education_id: int | None = None
    education_deleted: bool = False
    version: int | None = None

    def __post_init__(self) -> None:
        for name in ["education_title", "education_place", "education_end"]:
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip() or len(value) > 255:
                raise InvalidEducation(f"{name} must contain between 1 and 255 characters.")
        for name in [
            "education_title_es",
            "education_start",
            "education_start_es",
            "education_end_es",
        ]:
            value = getattr(self, name)
            if value is not None and (not isinstance(value, str) or len(value) > 255):
                raise InvalidEducation(f"{name} must be text with at most 255 characters.")
        if (
            type(self.education_position) is not int
            or not -(2**31) <= self.education_position < 2**31
        ):
            raise InvalidEducation("Education position must be a 32-bit integer.")
        if type(self.institution_id) is not int or self.institution_id <= 0:
            raise InvalidEducation("Institution ID must be positive.")
        if type(self.education_visible) is not bool or type(self.education_deleted) is not bool:
            raise InvalidEducation("Visibility and deletion state must be boolean.")
        if self.education_id is not None and (
            type(self.education_id) is not int or self.education_id <= 0
        ):
            raise InvalidEducation("Education ID must be positive.")
        if self.version is not None and (type(self.version) is not int or self.version < 0):
            raise InvalidEducation("Version must be a nonnegative integer.")
