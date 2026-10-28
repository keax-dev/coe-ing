# Tema: contrato para comprobar instituciones sin importar otra funcionalidad.

from typing import Protocol


class InstitutionLookup(Protocol):
    def exists_active(self, institution_id: int, *, lock: bool = False) -> bool: ...
