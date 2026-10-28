# Tema: pruebas automatizadas y casos límite.
# Comprobaremos resultados conocidos, listas vacías, montos inválidos y archivos incorrectos.
# Cada prueba debe indicar qué comportamiento esperamos, no copiar su implementación.
# unittest está incluido en Python; no hay que instalar herramientas externas.
# Los archivos de prueba se crean en carpetas temporales y se eliminan al terminar.
# Ejecuta: py lesson_21_testing.py

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from lesson_10_functions import calculate_balance, calculate_total, create_expense, format_money
from lesson_12_exceptions import parse_amount
from lesson_13_files import load_expenses, save_expenses
from lesson_15_algorithm_design import evaluate_expense
from lesson_18_searching_and_sorting import find_expense
from lesson_19_statistics import summarize_expenses
from lesson_20_nested_loops import calculate_monthly_totals


class ExpenseTrackerTests(unittest.TestCase):
    def test_total_of_known_expenses(self):
        expenses = [create_expense("Lunch", 1250), create_expense("Bus", 300)]
        self.assertEqual(calculate_total(expenses), 1550)

    def test_empty_expenses(self):
        self.assertEqual(calculate_total([]), 0)
        self.assertIsNone(summarize_expenses([])["average_cents"])
        self.assertIsNone(find_expense([], "Lunch"))

    def test_negative_balance_format(self):
        expenses = [create_expense("Lunch", 1250)]
        self.assertEqual(format_money(calculate_balance(1000, expenses)), "-$2.50")

    def test_invalid_amounts(self):
        for raw_amount in ["", "hello", "0", "-10", "12.50"]:
            # subTest identifica la entrada que falló y permite revisar las siguientes.
            with self.subTest(raw_amount=raw_amount):
                with self.assertRaises(ValueError):
                    parse_amount(raw_amount)

    def test_exact_budget_and_over_budget(self):
        self.assertTrue(evaluate_expense(1000, [], 1000)["accepted"])
        self.assertFalse(evaluate_expense(1000, [], 1001)["accepted"])

    def test_summary_of_known_expenses(self):
        expenses = [create_expense("Lunch", 1250), create_expense("Bus", 300)]
        self.assertEqual(summarize_expenses(expenses), {
            "count": 2, "total_cents": 1550, "average_cents": 775,
            "minimum_cents": 300, "maximum_cents": 1250,
        })

    def test_monthly_totals_include_empty_months(self):
        records = {"2026-09": {"food": [1250, 250], "transport": [300]}, "2026-10": {}}
        self.assertEqual(calculate_monthly_totals(records), {"2026-09": 1800, "2026-10": 0})

    def test_save_and_load(self):
        expenses = [create_expense("Lunch", 1250, "food")]
        with TemporaryDirectory() as directory:
            file_path = Path(directory) / "expenses.json"
            save_expenses(expenses, file_path)
            self.assertEqual(load_expenses(file_path), expenses)

    def test_invalid_saved_files(self):
        with TemporaryDirectory() as directory:
            file_path = Path(directory) / "expenses.json"
            for content in ["not JSON", "{}", '[{"description": "Lunch"}]']:
                with self.subTest(content=content):
                    file_path.write_text(content, encoding="utf-8")
                    with self.assertRaises(ValueError):
                        load_expenses(file_path)


if __name__ == "__main__":
    unittest.main(verbosity=2)
