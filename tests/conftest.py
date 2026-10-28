# Las fixtures proporcionan datos nuevos a cada prueba para evitar estado compartido.

import pytest

from expense_tracker.models import Expense
from expense_tracker.sample_data import sample_expenses


@pytest.fixture
def expenses() -> list[Expense]:
    return sample_expenses()
