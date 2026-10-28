# Tema: fixtures compartidas y aislamiento entre pruebas.

import pytest

from expense_tracker.models import Expense
from expense_tracker.sample_data import sample_expenses


@pytest.fixture
def expenses() -> list[Expense]:
    # La fixture se resuelve de nuevo en cada prueba para evitar datos mutables compartidos.
    return sample_expenses()
