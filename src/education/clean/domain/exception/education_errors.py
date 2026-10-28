# Tema: errores de negocio de educación sin dependencias externas.


class EducationError(Exception):
    pass


class InvalidEducation(EducationError, ValueError):
    pass


class EducationNotFound(EducationError):
    pass


class ActiveInstitutionNotFound(EducationError):
    pass


class EducationVersionConflict(EducationError):
    pass


class EducationPersistenceConflict(EducationError):
    pass


class EducationPersistenceFailure(EducationError):
    pass
