"""Unit tests. Run from the project root with:  python -m unittest discover tests"""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import file_manager as fm  # noqa: E402
from src import reports  # noqa: E402
from src.expense import Expense  # noqa: E402
from src.utils import validate_amount, validate_category, validate_date  # noqa: E402


def sample():
    return [
        Expense(100, "Food", "2024-01-05", "Tea"),
        Expense(300, "Food", "2024-01-06", "Lunch"),
        Expense(600, "Transport", "2024-02-01", "Cab"),
    ]


class TestExpense(unittest.TestCase):
    def test_creates_and_formats(self):
        expense = Expense("1500", "food", "2024-01-15", "Grocery")
        self.assertEqual(expense.amount, 1500.0)
        self.assertEqual(expense.category, "Food")
        self.assertEqual(expense.month, "2024-01")
        self.assertIn("Grocery", str(expense))

    def test_rejects_bad_values(self):
        with self.assertRaises(ValueError):
            Expense(-5, "Food", "2024-01-15")
        with self.assertRaises(ValueError):
            Expense(10, "Food", "15-01-2024")

    def test_round_trip_dict(self):
        expense = Expense(42.5, "Other", "2024-05-01", "Misc")
        self.assertEqual(Expense.from_dict(expense.to_dict()), expense)


class TestValidation(unittest.TestCase):
    def test_amount(self):
        self.assertEqual(validate_amount("1,500"), 1500.0)
        with self.assertRaises(ValueError):
            validate_amount("abc")

    def test_category(self):
        self.assertEqual(validate_category("transport"), "Transport")
        with self.assertRaises(ValueError):
            validate_category("Rocket")

    def test_date(self):
        self.assertEqual(validate_date("2024-01-15"), "2024-01-15")
        with self.assertRaises(ValueError):
            validate_date("2099-01-01")


class TestReports(unittest.TestCase):
    def test_totals_and_grouping(self):
        data = sample()
        self.assertEqual(reports.total(data), 1000)
        self.assertAlmostEqual(reports.average(data), 1000 / 3)
        self.assertEqual(reports.by_category(data)["Food"], 400)
        self.assertEqual(reports.by_month(data)["2024-02"], 600)

    def test_search_and_filter(self):
        data = sample()
        self.assertEqual(len(reports.search(data, "cab")), 1)
        self.assertEqual(len(reports.filter_month(data, "2024-01")), 2)


class TestFileManager(unittest.TestCase):
    def test_save_and_load(self):
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "expenses.csv")
            self.assertTrue(fm.save_expenses(sample(), path))
            self.assertEqual(fm.load_expenses(path), sample())

    def test_missing_file_is_empty(self):
        self.assertEqual(fm.load_expenses("/tmp/definitely-not-here.csv"), [])


if __name__ == "__main__":
    unittest.main()
