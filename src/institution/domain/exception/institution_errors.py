# Tema: errores del dominio sin estados HTTP ni excepciones de SQLAlchemy.


class InstitutionError(Exception):
    pass


class InvalidInstitution(InstitutionError, ValueError):
    pass


class InstitutionNotFound(InstitutionError):
    pass


class InstitutionVersionConflict(InstitutionError):
    pass


class InstitutionPersistenceConflict(InstitutionError):
    pass


class InstitutionPersistenceFailure(InstitutionError):
    pass
